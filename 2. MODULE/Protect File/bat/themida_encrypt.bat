@echo off
echo Starting Themida encryption...
set input_file=%1
set output_file=%2

REM sigcheck.exe로 파일 아키텍처 확인
C:\pymodules\sigcheck\sigcheck64.exe -a %input_file% > temp_arch.txt

REM temp_arch.txt에서 아키텍처 정보를 읽어옴
findstr /i "32-bit" temp_arch.txt > nul
if %errorlevel% == 0 (
    echo 32비트 파일입니다. Themida 32비트 버전으로 보호 작업을 실행합니다.
    "C:\Program Files (x86)\Themida Full Activated\Themida.exe" /protect "C:\Program Files (x86)\Themida Full Activated\Prevision.tmd" /inputfile %input_file% /outputfile %output_file%
    goto done
)

findstr /i "64-bit" temp_arch.txt > nul
if %errorlevel% == 0 (
    echo 64비트 파일입니다. Themida 64비트 버전으로 보호 작업을 실행합니다.
    "C:\Program Files (x86)\Themida Full Activated\Themida64.exe" /protect "C:\Program Files (x86)\Themida Full Activated\Prevision64.tmd" /inputfile %input_file% /outputfile %output_file%
    goto done
)

echo 파일 아키텍처를 확인할 수 없습니다. sigcheck 결과를 확인하세요.

:done
REM sigcheck 프로세스 종료 후 임시 파일 삭제

del temp_arch.txt
echo 작업 완료.
