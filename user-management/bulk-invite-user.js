/**
 * A script to bulk-invite users to Bridgecrew from a CSV file. By default, all accounts are assigned.
 * 
 * The following headers are required in the data: firstName,lastName,email,role,accounts
 * Usage: node bulk-invite-user.js --token <bridgecrew-api-key> --file <path to csv file> 
 */


const axios = require("axios");
const csv = require("fast-csv");
const fs = require("fs");
const path = require("path");
const program = require("commander");

program
  .description(
    "Tool to send bulk invitaions to users from a CSV file with headers firstName,lastName,email,role,accounts"
  )
  .option("--token <token>", "owner API token for org [required]")
  .option("--file <file>", "path to the CSV file [required]")
  .parse(process.argv);

if (!program.token) {
  console.error("Token is missing");
  program.help();
}

if (!program.file) {
  console.error("File is missing");
  program.help();
}

const run = async () => {
  const allAccounts = await getallAccounts(program.token);

  // Parse the CSV file containing user data
  fs.createReadStream(path.resolve(program.file))
    .pipe(csv.parse({ headers: true }))
    .on("error", (error) => console.error(error))
    .on("data", (user) => {
      // Assign list of all accounts
      if (user.accounts.toLowerCase() === "all") {
        user.accounts = allAccounts;
      }
      // Send invitation to the user
      sendInvitation(user, program.token);
    })
    .on("end", (rowCount) => console.log(`Parsed ${rowCount} rows`));
};

const sendInvitation = (user, token) => {
  console.log(`Sending invitation to ${user.email}`);
  const config = {
    method: "post",
    url: "https://www.bridgecrew.cloud/api/v1/invitation",
    headers: {
      Authorization: token,
      "Content-Type": "application/json; charset=UTF-8",
      Accept: "application/json, text/plain, */*",
    },
    data: user,
  };

  axios(config)
    .then((response) => {
      response.data
        ? console.log(response.data)
        : console.log(`✅ ${user.email}`);
    })
    .catch((error) => {
      console.error(`❌ ${user.email}`);
      console.error(
        `Error sending invite: ${JSON.stringify(error.response.data)}`
      );
    });
};

const getallAccounts = async (token) => {
  const config = {
    method: "get",
    url: "https://www.bridgecrew.cloud/api/v1/customers/accountIds",
    headers: {
      authorization: token,
    },
  };

  const data = await axios(config);
  console.log("List of all accounts:");
  console.log(Object.keys(data.data));
  return Object.keys(data.data);
};

run();
