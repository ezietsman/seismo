!
!  See deeming.py for info. This file contains 2 Fortran implimentations
!  of the deeming periodogram algorithm
subroutine periodogram(time, value, freqs, nt, nf , numprocs, amps)

! periodogram calculates the Deeming periodogram of the datapoints contained
! in the arrays time, value at the frequencies contained in freqs
! This subroutine is meant for f2py wrapping as well as a testbed of openMP
! within a python environment

    use omp_lib
    implicit none


    ! sizes of time and frequency arrays
    integer :: nt, nf, id
    ! arrays
    double precision time(nt), value(nt)
    double precision freqs(nf), amps(nf)
    integer :: numprocs, f
    double precision :: pi, realpart, imagpart

    pi = 3.1415926535897931D0
    realpart = 0.0D0
    imagpart = 0.0D0

! Add compiler directives so f2py knows what to do

!f2py intent(in) time
!f2py intent(in) value

!f2py intent(in) nt
!f2py depend(nt) time
!f2py depend(nt) value

!f2py intent(in) freqs
!f2py intent(in) nf
!f2py depend(nf) freqs

!f2py intent(in) numprocs
!f2py intent(out) amps

    call OMP_SET_NUM_THREADS(numprocs)

    !$OMP PARALLEL DO &
    !$OMP DEFAULT(SHARED) PRIVATE(f,realpart, imagpart)
    do f = 1, nf
        ! calculate real and imaginary parts
        realpart = sum((value*dcos(2.0D0*pi*freqs(f)*time)))
        imagpart = sum((value*dsin(2.0D0*pi*freqs(f)*time)))

        ! calculate the amplitude
        amps(f) = 2.0D0*dsqrt(realpart**2 + imagpart**2)/nt
    end do
    !$OMP END PARALLEL DO



end subroutine


subroutine periodogram2(time, value, freqs, nt, nf , numprocs, amps)

! periodogram calculates the Deeming periodogram of the datapoints contained
! in the arrays time, value at the frequencies contained in freqs
! This subroutine is meant for f2py wrapping as well as a testbed of openMP
! within a python environment

    use omp_lib
    implicit none


    ! sizes of time and frequency arrays
    integer :: nt, nf, id
    ! arrays
    double precision time(nt), value(nt)
    double precision freqs(nf), amps(nf)
    integer :: numprocs, f, d
    double precision :: pi, realpart, imagpart

    pi = 3.1415926535897931D0
    realpart = 0.0D0
    imagpart = 0.0D0

! Add compiler directives so f2py knows what to do

!f2py threadsafe
!f2py intent(in) time
!f2py intent(in) value

!f2py intent(in) nt
!f2py depend(nt) time
!f2py depend(nt) value

!f2py intent(in) freqs
!f2py intent(in) nf
!f2py depend(nf) freqs

!f2py intent(in) numprocs
!f2py intent(out) amps

    call OMP_SET_NUM_THREADS(numprocs)

    !$OMP PARALLEL DO &
    !$OMP DEFAULT(SHARED) PRIVATE(f,realpart, imagpart)
    do f = 1, nf
        ! calculate real and imaginary parts
        do d = 1, nt
            realpart = realpart + value(d)*dcos(2.0D0*pi*freqs(f)*time(d))
            imagpart = imagpart + value(d)*dsin(2.0D0*pi*freqs(f)*time(d))
        end do

        ! calculate the amplitude
        amps(f) = 2.0D0*dsqrt(realpart*realpart + imagpart*imagpart)/nt

        realpart = 0.0D0
        imagpart = 0.0D0
    end do
    !$OMP END PARALLEL DO

end subroutine
