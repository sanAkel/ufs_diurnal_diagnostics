program mnemonic_discovery
    implicit none
    character(len=255) :: infile
    character(len=8)   :: subset, found(100)
    integer            :: lungi, iret, nsub, i, n_found
    logical            :: new_type

    if (command_argument_count() < 1) stop "Usage: ./discovery <file>"
    call get_command_argument(1, infile)

    lungi = 10
    n_found = 0
    call datelen(10)
    
    open(lungi, file=trim(infile), form='unformatted')
    call openbf(lungi, 'IN', lungi)

    do while (.true.)
        call readmg(lungi, subset, nsub, iret)
        if (iret /= 0) exit
        
        new_type = .true.
        do i = 1, n_found
            if (subset == found(i)) new_type = .false.
        end do
        
        if (new_type .and. n_found < 100) then
            n_found = n_found + 1
            found(n_found) = subset
        end if
    end do

    print *, 'File: ', trim(infile)
    print *, 'Unique Mnemonics Found:'
    do i = 1, n_found
        print *, '  - ', found(i)
    end do
    call closbf(lungi)
end program mnemonic_discovery
