################################################################
#!powershell
# SCRIPT NAME: chkService.ps1
# PURPOSE: To check the Windows Service status
# AUTHOR: NetOne T.Urata
# WRITTEN DATE: 2017/02/22
# WANT_JSON
# POWERSHELL_COMMON
################################################################
$params = Parse-Args $Args;
$Ok= Get-Attr $params "RES_OK" $FALSE;
$Ng= Get-Attr $params "RES_NG" $FALSE;
$No_Arg= Get-Attr $params "NO_ARG" $FALSE;
#
$Serv = Get-Attr $params "SERVICE" $FALSE;
If ($Serv -eq $FALSE) {
    Fail-Json (New-Object psobject) $No_Arg ": SERVICE"
};
#

$State = Get-Attr $params "STATE" $FALSE;
If ($State -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": STATE"
};
#
$Mode = Get-Attr $params "MODE" $FALSE;
If ($Mode -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": MODE"
}
#;
#
function getService() {
   $err = "could not get service infomation!"
   $mes=New-Object System.Text.StringBuilder
   $ret=""
   $serv_title=" || Service Name : "
   $state_title=" || Status : "
   $mode_title=" || Mode : "
   try {
       $stat=get-wmiobject win32_service | Where-Object { $_.Name -eq $Serv } | %{$_.state}
       $mod=get-wmiobject win32_service | Where-Object { $_.Name -eq $Serv } | %{$_.startmode}
       $message=$mes.Append($serv_title+$Serv).ToString()
       $message=$mes.Append($state_title+$state).ToString()
       $message=$mes.Append($mode_title+$mode+" ").ToString()
       if ($stat -ne $null -And $stat -eq $State -And $mod -eq $Mode) {
           $message=$mes.Append($Ok).ToString()
           $result = New-Object psobject @{changed = $FALSE; $ret=$message }
       } else {
           $message=$mes.Append($Ng).ToString()
           $result = New-Object psobject @{failed = $TRUE; $ret="$message invalid value detected!" }
       }
   } catch {
       Fail-Json (New-Object psobject) $err
   } finally {
       Exit-Json $result;
   }
}
#
getService
