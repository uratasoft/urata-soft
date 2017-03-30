################################################################
#!powershell
# SCRIPT NAME: chkVcenter.ps1
# PURPOSE: To check vCenter setting
# WANT_JSON
# POWERSHELL_COMMON
################################################################
$params = Parse-Args $Args;
$Ok= Get-Attr $params "RES_OK" $FALSE;
$Ng= Get-Attr $params "RES_NG" $FALSE;
$No_Arg= Get-Attr $params "NO_ARG" $FALSE;
$server= Get-Attr $params "SERVER_NAME" $FALSE;
$user= Get-Attr $params "USER_NAME" $FALSE;
$pass= Get-Attr $params "PASS_WORD" $FALSE;
#
$Key = Get-Attr $params "KEY" $FALSE;
If ($Key -eq $FALSE){
    Fail-Json (New-Object psobject)  $No_Arg ": KEY"
};
#
function getVcenter() {
   $err = "could not get vcenter setting!"
   $mes=New-Object System.Text.StringBuilder
   $ret=""
   try {
       Add-PSSnapin VMware.VimAutomation.Core -ErrorAction Stop
       connect-viserver -server $server -user $user -Password $pass
       $keyval = $Key.Split(",")
       $keyword = $keyval[0]
       $valword  = $keyval[1]
       $deliword = " || "
       $dirword  = ": "
       $sinst = Get-View ServiceInstance
       $val=Get-View $sinst.Content.Setting | %{$_.setting} | Where-Object { $_.Key -eq $keyword } | %{$_.value}
       $message=$mes.Append($deliword+$keyword+$dirword).ToString()
       $message=$mes.Append($val).ToString()
       if ($val -eq $valword) {
           $result = New-Object psobject @{changed = $FALSE; $ret=$message }
       } else {
           $message=$mes.Append($Ng).ToString()
           $result = New-Object psobject @{failed = $TRUE; $ret="$message invalid value detected!" }
       }
   } catch {
       Fail-Json (New-Object psobject) $err
   } finally {
       Disconnect-VIServer -server $server
       Exit-Json $result;
   }
}
#
getVcenter
