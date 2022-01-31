# Usage

## bulk-invite-user

Below is sample csv file that is acceptable as input:

```csv
firstName,lastName,email,role,accounts
user,one,userone@example.com,developer,all
user,two,usertwo@example.com,developer,all
user,three,userthree@example.com,developer,all
```

You will need an API token with owner / admin permissions for the script to work. Example:

```sh
node bulk-invite-user.js --token <bridgecrew-api-key> --file <path-to-csv-file>
```
