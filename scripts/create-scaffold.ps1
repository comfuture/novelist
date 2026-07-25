$ErrorActionPreference = "Stop"
$ScriptPath = Join-Path $PSScriptRoot "create_scaffold.py"

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $ScriptPath @args
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 $ScriptPath @args
} else {
    & python $ScriptPath @args
}

exit $LASTEXITCODE
