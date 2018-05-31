; -- ifits-sftp.iss --
;
; This script shows various things you can achieve using a [Code] section for Uninstall

[Setup]
AppName=ifits-sftp
AppVersion=1.0
DefaultDirName=C:\Tools\ifits-sftp
DefaultGroupName=ifits-sftp
UninstallDisplayIcon={app}\ifits-sftp.exe
OutputDir=.\
Password=run?SFTS1!
Encryption=no


[Files]
Source: ".\*.tar.gz"; DestDir: "{app}"
Source: ".\*.cmd"; DestDir: "{app}"
Source: ".\*.md"; DestDir: "{app}"
Source: "..\..\*.txt"; DestDir: "{app}"
Source: ".\HooNetMeter.exe"; DestDir: "{app}"
Source: ".\README.md"; DestDir: "{app}"; Flags: isreadme

[Code]
function InitializeUninstall(): Boolean;
begin
  Result := MsgBox('InitializeUninstall:' #13#13 'Uninstall is initializing. Do you really want to start Uninstall?', mbConfirmation, MB_YESNO) = idYes;
  if Result = False then
    MsgBox('InitializeUninstall:' #13#13 'Ok, bye bye.', mbInformation, MB_OK);
end;

procedure DeinitializeUninstall();
begin
  //MsgBox('DeinitializeUninstall:' #13#13 'Bye bye!', mbInformation, MB_OK);
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  case CurUninstallStep of
    usUninstall:
      begin
        //MsgBox('CurUninstallStepChanged:' #13#13 'Uninstall is about to start.', mbInformation, MB_OK)
        // ...insert code to perform pre-uninstall tasks here...
      end;
    usPostUninstall:
      begin
        //MsgBox('CurUninstallStepChanged:' #13#13 'Uninstall just finished.', mbInformation, MB_OK);
        // ...insert code to perform post-uninstall tasks here...
      end;
  end;
end;
