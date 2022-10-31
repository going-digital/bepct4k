BITS 32

%include "4klang.inc"
extern __4klang_render@4

%macro WINAPI_FUNC 2
%if 1
	extern __imp__ %+ %1 %+ @ %+ %2
	%define %1 [__imp__ %+ %1 %+ @ %+ %2]
%else
	extern _ %+ %1 %+ @ %+ %2
	%define %1 _ %+ %1 %+ @ %+ %2
%endif
%endmacro

WINAPI_FUNC ExitProcess, 4
WINAPI_FUNC CreateFileA, 28
WINAPI_FUNC WriteFile, 20
WINAPI_FUNC CloseHandle, 4

GENERIC_READ EQU 0x80000000
GENERIC_WRITE EQU 0x40000000
FILE_SHARE_READ EQU 0x00000001
CREATE_ALWAYS EQU 2
FILE_ATTRIBUTE_NORMAL EQU 0x80

section _sndbuf bss align=1
sound_buffer: resd MAX_SAMPLES * 2
sound_buffer_end:

%macro FNCALL 1-*
	%rep %0-1
		%rotate -1
		push %1
	%endrep
	%rotate -1
	call %1
%endmacro

section _filename data align=1
filename: db 'music.raw', 0

section _text text align=1
_start:
	push	0
	push	FILE_ATTRIBUTE_NORMAL
	push	CREATE_ALWAYS
	push	0
	push	FILE_SHARE_READ
	push	GENERIC_WRITE
	push	filename
	push	sound_buffer
	FNCALL	__4klang_render@4
	FNCALL	CreateFileA
	push	eax
	push	0
	push	0
	push	sound_buffer_end - sound_buffer
	push	sound_buffer
	push	eax
	FNCALL	WriteFile
	FNCALL 	CloseHandle
	call 	ExitProcess
