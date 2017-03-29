################################################################
#!powershell
# SCRIPT NAME: chkRegistory.ps1
# PURPOSE: To set the Registory Entory
# AUTHOR: NetOne T.Urata
# WRITTEN DATE: 2017/02/22
# WANT_JSON
# POWERSHELL_COMMON
################################################################
$params = Parse-Args $Args;
$Ok= Get-Attr $params "RES_OK" $FALSE;
$Ng= Get-Attr $params "RES_NG" $FALSE;
$No_Arg= Get-Attr $params "NO_ARG" $FALSE;
$Regkey = Get-Attr $params "RKEY" $FALSE;
If ($Regkey -eq $FALSE){
   Fail-Json (New-Object psobject) $No_Arg ": RKEY"
};
#
$Rentory = Get-Attr $params "RENTORY" $FALSE;
If ($Rentory -eq $FALSE){
   Fail-Json (New-Object psobject) $No_Arg ": RENTORY"
};

$Rval = Get-Attr $params "RVAL" $FALSE;
If ($Rval -eq $FALSE){
    Fail-Json (New-Object psobject) $No_Arg ": RVAL"
};

#
function getRegistory() {
   $err = "could not get registory key!"
   $mes=New-Object System.Text.StringBuilder
   $reg_key=" || REGISTORY KEY: "
   $reg_entory=" || REGISTORY ENTORY: "
   $reg_val=" || REGISTORY VALUE: "
   $ret=""
#
   try {
       $rvalue=(Get-Item $Regkey).getvalue($Rentory)
       if ($rvalue -ne $null) {
           Set-ItemProperty $Regkey -Name $Rentory -Value $Rval
           $rvalue=(Get-Item $Regkey).getvalue($Rentory)
           if ($rvalue -eq $Rval) {
           $message=$mes.Append($reg_key+$Regkey+$reg_entory+$Rentory+$reg_val+$rvalue+" "+$Ok).ToString()
           $result = New-Object psobject @{changed = $FALSE; $ret=$message }
           }
       } else {
           $message=$mes.Append($reg_key+$Regkey+$reg_entory+$Rentory+$reg_val+$Rval+" "+$Ng).ToString()
           $result = New-Object psobject @{failed = $TRUE; $ret="$message invalid value detected!" }
       }
   } catch {
       Fail-Json (New-Object psobject) $err
   } finally {
       Exit-Json $result;
   }
}
#
getRegistory
