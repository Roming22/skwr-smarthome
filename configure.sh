#!/bin/bash
SCRIPT_DIR=`cd $(dirname $0); pwd`

SECRET="$SCRIPT_DIR/etc/secret.env"
[[ -e "$SECRET" ]] && source <(sed -e 's:=:=":' -e 's:$:":' $SECRET)

set_mandatory_value(){
	PROMPT=$2
	VAR=$1
	[[ -n "${!VAR}" ]] && DEFAULT="${!VAR}" || unset DEFAULT
	read -p "$PROMPT`[[ -n "$DEFAULT" ]] && echo -e " [$DEFAULT]"`: " INPUT
	export $VAR="${INPUT:-$DEFAULT}"
	[[ -z "${!VAR}" ]] && echo "Invalid value: Do not leave blank" && exit 1
	VAR_LIST="$VAR_LIST $VAR"
	unset INPUT
}

set_mandatory_password(){
	VAR=$1
	PROMPT=$2
	[[ -n "${!VAR}" ]] && DEFAULT="${!VAR}" || unset DEFAULT
	read -s -p "$PROMPT`[[ -n "$DEFAULT" ]] && echo -e " [leave blank to keep the current value]"`: " INPUT
	echo
	export $VAR="${INPUT:-$DEFAULT}"
	[[ -z "${!VAR}" ]] && echo "Invalid value: Do not leave blank" && exit 1
	VAR_LIST="$VAR_LIST $VAR"
	unset INPUT
}

write_secret(){
	VAR_LIST=( $VAR_LIST )
	for VAR in ${VAR_LIST[@]}; do
		echo "$VAR=${!VAR}"
	done > $SECRET
}

set_mandatory_value USERNAME "Enter the email account"
set_mandatory_password PASSWORD "Enter the password"
set_mandatory_value COUNTRY_CODE "Enter the country code"

write_secret
