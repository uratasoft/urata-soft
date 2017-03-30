################################################################
#!powershell
# SCRIPT NAME: chkOsServer.ps1
# PURPOSE: To check the Server and OS
# WANT_JSON
# POWERSHELL_COMMON
################################################################
$params = Parse-Args $Args;
$Ok= Get-Attr $params "RES_OK" $FALSE;
$Ng= Get-Attr $params "RES_NG" $FALSE;
$No_Arg= Get-Attr $params "NO_ARG" $FALSE;
#
$Group_Name = Get-Attr $params "GROUP_NAME" $FALSE;
If ($Group_Name -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": GROUP_NAME"
};
$Host_Name = Get-Attr $params "HOST_NAME" $FALSE;
If ($Host_Name -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": INV"
};
$Local_User = Get-Attr $params "LOCAL_USER" $FALSE;
If ($Local_User -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": LOCAL_USER"
};
#
function getHostName() {
   $err = "could not get host name!"
   $mes=New-Object System.Text.StringBuilder
   $mess_group=" || GROUP NAME : "
   $mess_host=" || HOST NAME : "
   $mess_user=" || LOCAL NAME : "
   $mess_domain=" || DOMAIN NAME : "
   $mess_version=" || VERSION : "
   $mess_serial=" || SERIAL NUMBER : "
   $ret=""
   $host=
   $message=$mes.Append($mess_group+$Group_Name).ToString()
   $message=$mes.Append($mess_host+$Host_Name).ToString()
   $message=$mes.Append($mess_user+$Local_User).ToString()
   $dom=Get-WmiObject Win32_ComputerSystem | %{ $_.Domain }
   $message=$mes.Append($mess_domain+$dom).ToString()
   $ver=Get-WmiObject Win32_OperatingSystem | %{ $_.version }
   $message=$mes.Append($mess_version+$ver).ToString()
   $ser=Get-WmiObject Win32_OperatingSystem | %{ $_.SerialNumber }
#
   try {
       $res=Get-CimInstance -ClassName Win32_GroupUser | select GroupComponent,PartComponent | select-string $Group_Name | select-string $Host_Name | Select-String $Local_User
       if ($res -ne $null) {
           $message=$mes.Append(" "+$Ok).ToString()
           $result = New-Object psobject @{changed = $FALSE; $ret=$message }
       } else {
           $message=$mes.Append(" "+$Ng).ToString()
           $result = New-Object psobject @{failed = $TRUE; $ret="$message invalid value detected!" }
       }
   } catch {
       Fail-Json (New-Object psobject) $host $err
   } finally {
       Exit-Json $result;
   }
}
#
getHostName
