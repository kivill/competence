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