sudo apt-get update -y;
sudo apt-get upgrade -y;
# Postgres repository
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main";
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - ;
sudo apt-get update -y;
sudo apt-get install git postgresql-9.6 virtualenv virtualenvwrapper libpq-dev libffi-dev python3-dev build-essential libssl-dev supervisor nginx ufw memcached libxmlsec1-dev pkg-config -y;
# Installing NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash ;
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
source ~/.profile
nvm install 14

# Creating DB
sudo su - postgres -c "psql -c \"CREATE USER admin WITH PASSWORD '2665640';\""
sudo su - postgres -c "psql -c \" ALTER USER "admin" with SUPERUSER;\""
sudo su - postgres -c "psql -c \" ALTER USER "admin" with CREATEROLE;\""
sudo su - postgres -c "psql -c \" ALTER USER "admin" with CREATEDB;\""
sudo su - postgres -c "createdb -e -O admin competence"

# Creating virtualenv for python-backend
cd $project_folder
echo "virtualenv for python-backend will be created!"
echo "Creating virtualenv named $virtenv_name!"
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> ~/.bashrc
export WORKON_HOME=~/.virtualenvs
mkdir $WORKON_HOME
echo "export WORKON_HOME=$WORKON_HOME" >> ~/.bashrc
echo "export PIP_VIRTUALENV_BASE=$WORKON_HOME" >> ~/.bashrc
source ~/.bashrc
export WORKON_HOME=~/.virtualenvs
mkvirtualenv -q -p /usr/bin/python3 competence
deactivate
echo "virtualenv for python-backend created!"

# Creating .env files
workon competence
rm $VIRTUAL_ENV/bin/postactivate
sed -i -e 's/\r$//' .env/postactivate
ln -s `pwd`/.env/postactivate $VIRTUAL_ENV/bin/postactivate
rm $VIRTUAL_ENV/bin/predeactivate
sed -i -e 's/\r$//' .env/predeactivate
ln -s `pwd`/.env/predeactivate $VIRTUAL_ENV/bin/predeactivate
deactivate