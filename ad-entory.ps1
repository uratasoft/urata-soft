$pwd = ConvertTo-SecureString -AsPlainText -Force gAbcd0123h
$cred = New-Object System.Management.Automation.PSCredential(gadtan\JoinAccounth,$pwd)

Add-Computer -DomainName adtan -Credential $cred


PS Z:\> $ComputerSystem = Get-WmiObject Win32_ComputerSystem

PS Z:\> Write-Host -NoNewline "Domain/Workgroup : "
    if( $ComputerSystem.PartOfDomain -eq $True ){
        Write-Host "Domain"
        Write-Host -NoNewline "Domain name : "
    }
    else{
        Write-Host "Workgroup"
        Write-Host -NoNewline "Workgroup name : "
    }
    Write-Host $ComputerSystem.Domain

Domain/Workgroup : Domain
Domain name : noswin.netone.co.jp