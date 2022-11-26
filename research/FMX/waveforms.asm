bits 32

; wf input -1 to 1, output -1 to 1 nominal
wf_all_3dBoct:
    ; All harmonics, bright 1/n harmonics
    ; Input: st0 contains phase 0-1
    ; Output: st0 contains wave, 1 to -1 dc balanced
    ; This is a sawtooth
    ret

wf_all_6dBoct:
    ; All harmonics, mellow 1/n2 harmonics
    ; This is a dc adjusted parabola
    ; Input: st0 contains phase 0-1
    fabs
    fmul    st0, st0
    fadd    st0, st0
    fsub    dword [c_0_355]
    ; Output: st0 contains wave -1 to 1
    ret

wf_odd_3dBoct:
    ; Odd harmonics, bright 1/n harmonics
    ; Square wave
    ;?
    ret

wf_odd_6dBoct:
    ; Odd harmonics, mellow 1/n2 harmonics
    ; Triangle wave
    fabs
    fadd    st0, st0
    fld1
    fsubrp
    ret

wf_even_3dBoct:
    fldpi                   ; pi, x
    fmul                    ; pi x, x
    fcos                    ; cos(pi x), x
    fxchg                   ; x, cos(pi x)
    fld1                    ; 1, x, cos(pi x)
    fxchg                   ; x, 1, cos(pi x)
    fadd                    ; x+1, 1, cos(pi x)
    fprem1                  ; (x+1) % 1, 1, cos(pi x)
    fstp st1                ; (x+1) % 1, cos(pi x)
    fsub dword [c_0_5]
    faddp
    ret

wf_even_6dBoct:
    fldpi                   ; pi, x
    fmul                    ; pi x, x
    fcos                    ; cos(pi x), x
    fxchg                   ; x, cos(pi x)
    fld1                    ; 1, x, cos(pi x)
    fxchg                   ; x, 1, cos(pi x)
    fadd                    ; x+1, 1, cos(pi x)
    fprem1                  ; (x+1) % 1, 1, cos(pi x)
    fstp st1                ; (x+1) % 1, cos(pi x)
    fmul st0, st0
    fsub dword [c_0_355]
    faddp
    ret

