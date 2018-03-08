#!/bin/bash
HOSTNAME=$(hostname)
mmcli -m 0 > /tmp/${HOSTNAME}_log.txt
REFRESH_TOKEN="1/j06fxt0YkYtrQEBUvKd_ILHsX_l2T7LN84FRG1uuZoeUQTEz3fEbIOXusFQoJRJI"
CLIENT_ID="761866041142-ss6v9qaiq0oel3esqm81enbf0k24dvh1.apps.googleusercontent.com"
CLIENT_SECRET="H4bQe1RaElK6WXUfirfHSdEF"
META_DATA="{\"title\": \"${HOSTNAME}_log.txt\",\"mimeType\": \"text/plain\",\"description\": \"Uploaded From Curl\"}"
GET_TOKEN_RESULT=$(curl -X POST https://accounts.google.com/o/oauth2/token \
-d "code=4/AABAfsXzHlu1ZdihEuniS4JkHqebX5OE-rvdTJbF2nMCPtQY0ybBO8k" \
-d "client_id=761866041142-ss6v9qaiq0oel3esqm81enbf0k24dvh1.apps.googleusercontent.com" \
-d "client_secret=H4bQe1RaElK6WXUfirfHSdEF" \
-d "redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
-d "grant_type=authorization_code")
echo $GET_TOKEN_RESULT >> /tmp/${HOSTNAME}_log.txt
function upload_file () {
    #ホストネームがファイル名のlog.txtをアップロード
    curl -X POST https://www.googleapis.com/upload/drive/v2/files?uploadType=multipart \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: multipart/related" \
    -F "metadata=$META_DATA;type=application/json;charset=UTF-8" \
    -F "file=@${HOSTNAME}_log.txt;type=text/plain"
}

function refresh_access_token (){
    #アクセストークン期限切れ時にリフレッシュ
    ACCESS_TOKEN=$(curl -X POST https://accounts.google.com/o/oauth2/token \
    -d "refresh_token=$REFRESH_TOKEN" \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "grant_type=refresh_token"|grep "access_token" |cut -d ":" -f 2|sed -e "s/^\"//g"|sed -e "s/\",$//g")
}

#ACCESS_TOKEN発行済とACCESS_TOKENが間違っていてエラーした場合の見分けが付かないので、毎回リフレッシュする
refresh_access_token
upload_file
exit 0
