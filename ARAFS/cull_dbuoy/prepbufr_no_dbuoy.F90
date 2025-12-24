!==============================================================================
! PROGRAM: prepbufr_no_dbuoy
! 
! DEVELOPER NOTE ON BUFRLIB LIMITATIONS:
! This code contains intentionally redundant logic to compensate for legacy
! BUFRLIB behavior. 
! 1. It targets both 'TYP' and 'T29' because mnemonic naming is inconsistent.
! 2. It implements a dual-mode filter: 'Block Mode' (COPYMG) for speed/integrity
!    of non-target data, and 'Surgical Mode' (READSB/WRITSB) for surface data.
! 3. Manual message closing (CLOSMG) is required to prevent library aborts
!    when switching between subset and message level operations.
!==============================================================================

program prepbufr_no_dbuoy
    implicit none

    character(len=255) :: infile, outfile
    character(len=8)   :: subset
    integer            :: lungi, lungm, iret, iretsb, idate
    integer            :: n_dbuoy, n_kept_shp, n_total
    real*8             :: val_typ(1), val_t29(1), bmiss
    
    n_dbuoy = 0 ; n_kept_shp = 0 ; n_total = 0
    lungi = 80 ; lungm = 81
    bmiss = 10.0**10 ! BUFRLIB standard missing value

    call get_command_argument(1, infile)
    call get_command_argument(2, outfile)

    ! Set 10-digit date handling (YYYYMMDDHH)
    call datelen(10)
    
    open(lungi, file=trim(infile), form='unformatted', status='old')
    open(lungm, file=trim(outfile), form='unformatted', status='replace')

    ! Open input and use it as the dictionary template for output
    call openbf(lungi, 'IN',  lungi)
    call openbf(lungm, 'OUT', lungi)

    print *, '  [STDOUT] Filter: Inspecting Surface Categories for 564s...'

    do while (.true.)
        call readmg(lungi, subset, idate, iret)
        if (iret /= 0) exit 
        
        ! Only perform expensive subset-level surgery on Marine/Surface categories
        if (subset == 'SFCSHP' .or. subset == 'ADPSFC') then
            call openmg(lungm, subset, idate)
            
            do while (.true.)
                call readsb(lungi, iretsb)
                if (iretsb /= 0) exit 

                n_total = n_total + 1
                val_typ(1) = bmiss
                val_t29(1) = bmiss

                ! Redundant extraction because mnemonics vary by Prepbufr version
                call ufbint(lungi, val_typ, 1, 1, iret, 'TYP')
                call ufbint(lungi, val_t29, 1, 1, iret, 'T29')

                ! CULL LOGIC: Target Drifting Buoys (564)
                if (nint(val_typ(1)) == 564 .or. nint(val_t29(1)) == 564) then
                    n_dbuoy = n_dbuoy + 1
                else
                    ! Manually pack the report into the output buffer
                    call writsb(lungm)
                    n_kept_shp = n_kept_shp + 1
                end if
            end do
            call closmg(lungm) ! Explicitly flush the surgical message
        else
            ! Fast-track other categories (SATWND, ADPUPA, etc.) as raw blocks
            call copymg(lungi, lungm)
        end if
    end do

    call closbf(lungi) ; call closbf(lungm)
    close(lungi) ; close(lungm)
    
    print *, '  ---------------------------------------------------------'
    print *, '  CULL RESULTS FOR: ', trim(infile)
    print *, '  Total Surface Reports Scanned: ', n_total
    print *, '  Drifting Buoys (564) DROPPED:  ', n_dbuoy
    print *, '  Reports (Ships/Etc) PRESERVED: ', n_kept_shp
    print *, '  ---------------------------------------------------------'

end program prepbufr_no_dbuoy
