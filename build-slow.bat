if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )

set LIBS= /LIBPATH:libs opengl32.lib winmm.lib kernel32.lib user32.lib gdi32.lib
set OPTS= ^
	/ENTRY:start ^
	/CRINKLER ^
	/SUBSYSTEM:WINDOWS ^
	/UNSAFEIMPORT ^
	/NOINITIALIZERS ^
	/RANGE:opengl32 ^
	/PRINT:IMPORTS ^
	/PRINT:LABELS ^
	/TRANSFORM:CALLS ^
	/TINYIMPORT

REM very slow unpack, avoid /TINYHEADER

shader_minifier.exe --format nasm -o shader.inc shader.frag || exit /b 1
nasm.exe -fwin32 -o intro.obj intro.asm || exit /b 2
nasm.exe -fwin32 -o 4klang.obj 4klang.asm || exit /b 3

crinkler.exe ^
	%OPTS% ^
	/COMPMODE:SLOW /ORDERTRIES:16000 /REPORT:report-slow.html ^
	%LIBS% ^
	intro.obj 4klang.obj /OUT:intro-slow.exe ^
	|| exit /b 2
