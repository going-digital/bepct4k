bits 32

c_0_333:
    dd      0.33333
c_0.5:
    dd      0.5
c_0.667:
    dd      0.66667

%macro wf_all_3dBoct
    ; All harmonics, diminishing by 1/n, 0 bytes
    ; No instructions needed, as phase is already sawtooth
%endmacro

%macro wf_all_6dBoct
    ; All harmonics, diminishing by 1/n^2, 10 bytes, uses 0 stack
    ; Parabolic wave
    fmul    st0, st0
    fadd    st0, st0
    fsub    dword [c_0_667] ; dc balancing
%endmacro

%macro wf_sine
    ; Pure fundamental only, 6 bytes, uses 1 stack
    ; Sine wave
    fldpi
    fmulp
    fcos
%endmacro

%macro wf_odd_3dBoct
    ; Odd harmonics, diminishing by 1/n, 16 bytes, uses 1 stack
    ; Square wave
    fldz                ; 0, x
    fcomip  st0, st1    ; x
    fstp    st1         ; empty
    fld1                ; 1
    fld1                ; 1, 1
    fchs                ; -1, 1
    fcmovb  st0, st1    ; 1 or -1, -1
    fstp    st1         ; 1 or -1
%endmacro

%macro wf_odd_6dBoct
    ; Odd harmonics, diminishing by 1/n2, 8 bytes, uses 1 stack
    ; Triangle wave
    fabs
    fadd    st0, st0
    fld1
    fsubrp
%endmacro

%macro wf_even_3dBoct
    ; Even harmonics, diminishing by 1/n, 26 bytes, uses 2 stack
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
%endmacro

%macro wf_even_6dBoct
    ; Even harmonics, diminishing by 1/n2, 28 bytes, uses 2 stack
    fldpi                   ; pi, x
    fmul                    ; pi x, x
    fcos                    ; cos(pi x), x
    fxchg                   ; x, cos(pi x)
    fld1                    ; 1, x, cos(pi x)
    fxchg                   ; x, 1, cos(pi x)
    fadd                    ; x+1, 1, cos(pi x)
    fprem1                  ; (x+1) % 1, 1, cos(pi x)
    fstp    st1                ; (x+1) % 1, cos(pi x)
    fmul    st0, st0
    fsub    dword [c_0_333]
    faddp
%endmacro

%macro phasor
    fld1                    ; 1
    fld     dword [esi]     ; oldph, 1 Read old phase
    fadd    dword [edi]     ; newph, 1 Read velocity
    add     edi, 4
    fprem1                  ; newph % 1, 1
    fstp    st1             ; newph % 1
    fst     dword [esi]     ; Update phase
    add     esi, 4
%endmacro

%macro fm_phasor
    fld1                    ; 1, x
    fld     dword [esi]     ; oldph, 1, x
    fadd    dword [edi]
    add     edi, 4
    fadd    st2             ; newph, 1, x
    fprem1                  ; newph % 1, 1, x
    fstp    st1             ; newph % 1, x
    fstp    st1             ; newph % 1
    fst     dword [esi]     ; Update phase
    add     esi, 4
%endmacro

%macro gain_block
    fld     dword [edi]
    fmulp
    add     edi, 4
%endmacro

formant_synth:
    phasor          ; Formant frequency
    gain_block      ; Formant bandwidth
    phasor          ; Formant frequency
    gain_block      ; Formant bandwidth
    faddp
    phasor          ; Formant frequency
    gain_block      ; Formant bandwidth
    faddp
    wf_all_6dBoct
    fm_phasor
