# Election-Website User Manual
University Dissertation - Registration and Voting Website for an Election with Blockchain

# Operating System Shared Downloads

This section lists the requirements for the system that are shared by both main operating systems.

The first requirement is having either the Google Chrome or Mozilla Firefox browser as these are the browsers 
that can operate the MetaMask extension.

The next requirement is Chrome or Mozilla’s MetaMask extension for injecting blockchain accounts into 
websites, these are respectively found at:
https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn
https://addons.mozilla.org/en-US/firefox/addon/ether-metamask

The final shared requirement is Truffle’s Ganache GUI for local blockchain development found at:
http://truffleframework.com/ganache/

This guide assumes that git is installed on the target machine, in order to download the source code for this 
software run the command:
"git clone https://github.com/LukeDeBeneducci/Election-Website"

# Windows Installation

First to install the required packages for using the software we will use the command line package manager Chocolatey. Found at
https://chocolatey.org/ this can be installed by following the instructions on the website or from an administrator command prompt via:

@”%SystemRoot%32ˇ1.0.exe”  -NoProfile  -InputFormat  None  -ExecutionPolicy  Bypass  -Command  ”iex((New-Object System.Net.WebClient).
DownloadString(’https://chocolatey.org/install.ps1’))”  SET ”PATH=%PATH%;%ALLUSERSPROFILE%”

Now  we  must  install  Python2,  Python  Package  Index,  Nodejs,  PostgreSQL,  and  Truffle.   
We  can  do this by running the following commands.  Note that to access npm and psql you might have to re-opencommand prompt.

choco install python2
choco install pip
choco install nodejs
choco install postgresql
npm install -g truffle

The next stage is to set up our local Postgres database for storing users.  To do this in the cmd promptrun the command 
"psql  -U  postgres" the program will ask for a password the default password should be Postgres1234. 
Inside of the psql terminal run the command "CREATE  DATABASE  election_web;" 
oncethe terminal responds that a database was created run "\q" to quit the psql command line interface.

From  here  migrate  to  the  main  directory  for  the  Election-Website  project  code  and  run  the  following commands:

pip install -r requirements.txt
Set APPSETTINGS=config.DevelopmentConfig
Set DATABASEURL=postgresql://postgres:Postgres1234@localhost/electionweb

# MacOS Installation

First to install the required packages for using the software we will use the command line package manager HomeBrew. 
Found at https://brew.sh this can be installed by following the instructions on the website or from the terminal via

/usr/bin/ruby -e ”$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)”

Now  we  must  install  Python2,  Python  Package  Index,  Nodejs,  PostgreSQL,  and  Truffle.   
We  can  do this by running the following commands.  

brew install python@2
brew install nodejs
brew install postgresql
npm install -g truffle

The next stage is to set up our local Postgres database for storing users.  To do this in the terminal run the command psql.  
Inside of the psql terminal run the command "CREATE DATABASE electionweb;" once the terminal responds that a database was 
created run "\q" to quit the psql command line interface. 
From  here  migrate  to  the  main  directory  for  the  Election-Website  project  code  and  run  the  following commands:

pip install -r requirements.txt
export APPSETTINGS=”config.DevelopmentConfig”
export DATABASEURL=”postgresql://*user*@localhost/electionweb”  (where *user* is your Mac user account)

# Running the Program

All of the below require Ganache to be open, whilst Ganache is open it maintains your local blockchain.
In order to vote with the smart contract you must first set up MetaMask, to do this find the extension icon in your
browser of choice, accept the terms of use and select a password for your new vault.  You will be given a 12 word seed 
phrase to save that you can use to restore all accounts for your vault.  

From inside the MetaMask extension on the top left click on the Main Network drop down and instead select Custom RPC, 
set the Custom RPC URL as "http://localhost:7545". 

Now  migrate  to  the  Elections  folder  located  at Election-Website/project/static/Election and  run  the following  
command "truffle.cmd  migrate  --reset" in  order  to  run  a  creation  call  for  the  smart  contract. 

From the main project directoryElection-Website you should now be able to run the command "python run.py" the website 
should now be available at the URL localhost:5000. 

To import an account from the Ganache test blockchain network into MetaMask you must first get the account’s private key, 
this is found in Ganache by pressing the key icon on the far right of the account list.  Then from the MetaMask window 
select the account drop down window from the icon on the top right and choose Import Account.

You can now vote on the website, note that there is only one vote per account on both the user-side and the blockchain-side.  
In order to cast another vote you will need to re-register another account and also import another Ethereum account from Ganache.
