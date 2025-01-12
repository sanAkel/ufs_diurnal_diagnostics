#!/bin/csh -f

set iter = 1

while (${iter} <= 11)
  echo ${iter}
  python time-forecast_error_day.py
  set iter = `expr ${iter} + 1`
end
