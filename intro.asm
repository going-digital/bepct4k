BITS 32

WIDTH equ 1920
HEIGHT equ 1080

SIZEOF_FLOAT equ 4
STEREO_CHANNELS equ 2

%ifndef DEBUG
%define FULLSCREEN
%define AUDIO_THREAD
%define GLCHECK
%else
%define NO_AUDIO
%macro GLCHECK 0
	call glGetError
	test eax, eax
	jz %%ok
	int 3
%%ok:
%endmacro
%endif

%ifndef NO_AUDIO
%include "4klang.inc"
extern __4klang_render@4
%else
%define SAMPLE_RATE 44100
%define MAX_SAMPLES 44100*120
%define SAMPLES_PER_TICK 44100/16
%endif

;GL_TEXTURE_2D EQU 0x0de1
GL_FRAGMENT_SHADER EQU 0x8b30
;GL_UNSIGNED_BYTE EQU 0x1401
;GL_FLOAT EQU 0x1406
;GL_RGBA EQU 0x1908
;GL_LINEAR EQU 0x2601
;GL_TEXTURE_MIN_FILTER EQU 0x2801
;GL_RGBA16F EQU 0x881a
;GL_FRAMEBUFFER EQU 0x8d40
;GL_COLOR_ATTACHMENT0 EQU 0x8ce0

%macro WINAPI_FUNC 2
%if 1
	extern __imp__ %+ %1 %+ @ %+ %2
	%define %1 [__imp__ %+ %1 %+ @ %+ %2]
%else
	extern _ %+ %1 %+ @ %+ %2
	%define %1 _ %+ %1 %+ @ %+ %2
%endif
%endmacro

%ifdef FULLSCREEN
WINAPI_FUNC ChangeDisplaySettingsA, 8
%endif
%ifdef AUDIO_THREAD
WINAPI_FUNC CreateThread, 24
%endif
%ifdef DEBUG
WINAPI_FUNC MessageBoxA, 16
%endif
WINAPI_FUNC ChoosePixelFormat, 8
WINAPI_FUNC CreateWindowExA, 48
WINAPI_FUNC ExitProcess, 4
WINAPI_FUNC GetAsyncKeyState, 4
WINAPI_FUNC GetDC, 4
WINAPI_FUNC PeekMessageA, 20
WINAPI_FUNC SetPixelFormat, 12
WINAPI_FUNC ShowCursor, 4
WINAPI_FUNC SwapBuffers, 4
WINAPI_FUNC waveOutGetPosition, 12
WINAPI_FUNC waveOutOpen, 24
WINAPI_FUNC waveOutWrite, 12
WINAPI_FUNC wglCreateContext, 4
WINAPI_FUNC wglGetProcAddress, 4
WINAPI_FUNC wglMakeCurrent, 8
;WINAPI_FUNC glGenTextures, 8
;WINAPI_FUNC glBindTexture, 8
;WINAPI_FUNC glTexImage2D, 36
;WINAPI_FUNC glTexParameteri, 12
WINAPI_FUNC glRects, 16
%ifdef DEBUG
WINAPI_FUNC glGetError, 0
%endif

%macro FNCALL 1-*
	%rep %0-1
		%rotate -1
		push %1
	%endrep
	%rotate -1
	call %1
%endmacro

%macro GL_FUNC 1
section _ %+ %1 data align=1
%1:
%defstr %[%1 %+ __str] %1
	db %1 %+ __str, 0
%endmacro

GL_FUNC glCreateShaderProgramv
GL_FUNC glUseProgram
GL_FUNC glGetUniformLocation
;GL_FUNC glUniform1i
GL_FUNC glUniform1f
;GL_FUNC glGenFramebuffers
;GL_FUNC glBindFramebuffer
;GL_FUNC glFramebufferTexture2D
;GL_FUNC glUniform1fv

%ifdef DEBUG
GL_FUNC glGetProgramInfoLog
%endif

%ifdef DEBUG
	WNDCLASS EQU static_
%else
	%define WNDCLASS 0xc018
%endif

%ifdef FULLSCREEN
section _devmode data align=1
devmode:
    ; DEVMODE structure
    ; https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-devmodea
    times 32 db 0   ; dmDeviceName
    dw      0       ; dmSpecVersion
    dw      0       ; dmDriverVersion
    dw      0x9c    ; dmSize
    dw      0       ; dmDriverExtra
    dd      0x1c0000 ; dmFields
    dd      0, 0    ; dmPosition
    dd      0       ; dmDisplayOrientation
    dd      0       ; dmDisplayFixedOutput
    dw      0       ; dmColor
    dw      0       ; dmDuplex
    dw      0       ; dmYResolution
    dw      0       ; dmTTOPtion
    dw      0       ; dmCollate
    times 32 db 0   ; dmFormName
    dw      0       ; dmdmLogPixels
    dd      0x20    ; dmBitsPerPel
    dd      WIDTH   ; dmPelsWidth
    dd      HEIGHT  ; dmPelsHeight
    dd      0       ; dmDisplayFlags
    dd      0       ; dmDisplayFrequency
    dd      0       ; dmICMMethod
    dd      0       ; dmICMIntent
    dd      0       ; dmMediaType
    dd      0       ; dmDitherType
    dd      0       ; dmReserved1
    dd      0       ; dmReserved2
    dd      0       ; dmPanningWidth
    dd      0       ; dmPanningHeight
%endif

section _pfd data align=1
pfd:
    ; PIXELFORMATDESCRIPTOR structure
    ; https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-pixelformatdescriptor
    dw      0       ; nSize should be sizeof(PIXELFORMATDESCRIPTOR) (0x28)
    dw      0       ; nVersion should be 1 (0x01)
    dd      0x21    ; dwFlags PFD_SUPPORT_OPENGL + PFD_DOUBLEBUFFER
    db      0       ; iPixelType
    db      0       ; cColorBits (0x20)
    db      0       ; cRedBits
    db      0       ; cRedShift
    db      0       ; cGreenBits
    db      0       ; cGreenShift
    db      0       ; cBlueBits
    db      0       ; cBlueShift
    db      0       ; cAlphaBits
    db      0       ; cAlphaShift
    db      0       ; cAccumBits
    db      0       ; cAccumRedBits
    db      0       ; cAccumGreenBits
    db      0       ; cAccumBlueBits
    db      0       ; cAccumAlphaBits
    db      0       ; cDepthBits (0x20)
    db      0       ; cStencilBits
    db      0       ; cAuxBuffers
    db      0       ; iLayerType
    db      0       ; bReserved
    dd      0       ; dwLayerMask
    dd      0       ; dwVisibleMask
    dd      0       ; dmDamageMask

section _wavefmt data align=1
wavefmt:
    ; WAVEFORMATEX
    ; https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex
	dw		3 ; wFormatTag = WAVE_FORMAT_IEEE_FLOAT
	dw		STEREO_CHANNELS ; nChannels
	dd		SAMPLE_RATE ; nSamplesPerSec
	dd		SAMPLE_RATE * SIZEOF_FLOAT * STEREO_CHANNELS; nAvgBytesPerSec
	dw		SIZEOF_FLOAT * STEREO_CHANNELS ; nBlockAlign
	dw		8 * SIZEOF_FLOAT ; wBitsPerSample
	dw		0 ; cbSize

section _wavehdr data align=1
wavehdr:
	dd		sound_buffer ; lpData
	dd		MAX_SAMPLES * STEREO_CHANNELS * SIZEOF_FLOAT ; dwBufferLength
    dd      0       ; dwBytesRecorded
    dd      0       ; dwUser
	dd 		2 		; dwFlags WHDR_PREPARED  =  0x00000002
    dd      0       ; dwLoops
    dd      0       ; *lpNext
    dd      0       ; reserved
	wavehdr_size EQU ($ - wavehdr)

section _mmtime bss align=1
mmtime:
    resd    1       ; ms
    resd    1       ; sample
    resd    1       ; cb
    resd    1       ; ticks
    resb    8       ; smpte hour, min, sec, frame, fps, dummy, pad1, pad2

section _waveout bss align=1
waveout: resd 8

section _sndbuf bss align=1
tmp:
sound_buffer: resd MAX_SAMPLES * 2

%ifdef DEBUG
section _infolog bss align=1
infolog: resb 1024
%endif

section _shader data align=1
%if 1
%include "shader.inc"
%else
_shader_frag:
	db 'uniform int t;'
	db 'float t = t/44100.;'
	db 'void main(){gl_FragColor = vec4(sin(t));}'
%endif

section _shdrptr data align=1
src_main:
	dd _shader_frag

section _strings data align=1
%ifdef DEBUG
static_: db "static", 0
%endif

section _text text align=1
_start:
%if 0
	%define ZERO 0
%else
	%define ZERO ecx
	xor 	ZERO, ZERO
%endif
	; Prepopulate stack for as much as possible
	; This clusters the pushes, which helps the compressor.
	push 	wavehdr_size
	push 	wavehdr
	push 	ZERO
	push 	ZERO
	push 	ZERO
	push 	wavefmt
	push 	byte -1
	push 	waveout
	push 	pfd
	push 	pfd
	push 	ZERO
	push 	ZERO
	push 	ZERO
	push 	ZERO
	push 	HEIGHT
	push 	WIDTH
	push 	ZERO
	push 	ZERO
	push 	0x90000000
	push 	ZERO
	push 	WNDCLASS
	push 	ZERO
	push 	ZERO
%ifdef FULLSCREEN
	push 	4
	push 	devmode
%endif
%ifndef NO_AUDIO
%ifdef AUDIO_THREAD
	push 	ZERO
	push 	ZERO
	push 	sound_buffer
	push	__4klang_render@4
	push	ZERO
	push	ZERO
%endif
%endif
%ifndef NO_AUDIO
%ifdef AUDIO_THREAD
	FNCALL 	CreateThread
%else
	push sound_buffer
	FNCALL 	__4klang_render@4
%endif
%endif
%ifdef FULLSCREEN
	FNCALL 	ChangeDisplaySettingsA
%endif
	FNCALL 	ShowCursor
	FNCALL 	CreateWindowExA
	push 	eax
	FNCALL 	GetDC
	mov 	ebp, eax ; ebp = HDC
	push 	eax
	FNCALL 	ChoosePixelFormat
	push 	eax
	push 	ebp
	FNCALL 	SetPixelFormat
	push 	ebp
	FNCALL 	wglCreateContext
	push 	eax
	push 	ebp
	FNCALL 	wglMakeCurrent
	GLCHECK
	push 	src_main
	push 	1
	push 	GL_FRAGMENT_SHADER
	push 	glCreateShaderProgramv
	FNCALL 	wglGetProcAddress
	FNCALL 	eax
%ifdef DEBUG
	push 	eax
	push 	infolog
	push 	0
	push 	1023
	push 	eax
	FNCALL 	wglGetProcAddress, glGetProgramInfoLog
	call 	eax
	push 	0
	push 	infolog
	push 	infolog
	push 	0
	call 	MessageBoxA
	pop 	eax
%endif
	mov 	esi, eax
	FNCALL 	wglGetProcAddress, glUseProgram
	FNCALL 	eax, esi
	GLCHECK

	; PLAY MUSIC
	FNCALL 	waveOutOpen
	push 	dword [waveout]
	FNCALL 	waveOutWrite

mainloop:
	FNCALL 	waveOutGetPosition, dword [waveout], mmtime, 12
	mov 	ebx, dword [mmtime + 4]
	cmp 	ebx, MAX_SAMPLES * 8
	jge 	exit

	push 	0x1b ;GetAsyncKeyState

	; PeekMessageA
	push 	1
	push 	ZERO
	push 	ZERO
	push 	ZERO
	push 	ZERO

	; SwapBuffers
	push 	ebp

	; glRects
	push 	1
	push 	1
	push 	byte -1
	push 	byte -1

	push 	ebx
	fild 	dword [esp]
	push 	SAMPLES_PER_TICK * 8 * 4
	fild 	dword [esp]
	fdivp
	pop 	ebx
	fstp 	dword [esp]
	push 	_var_T
	push 	esi
	push 	glGetUniformLocation
	call 	wglGetProcAddress
	call 	eax
	push 	eax
	push 	glUniform1f
	call 	wglGetProcAddress
	call 	eax
	call 	glRects
	call 	SwapBuffers
	call 	PeekMessageA
	call 	GetAsyncKeyState
	jz		mainloop
exit:
	call 	ExitProcess
