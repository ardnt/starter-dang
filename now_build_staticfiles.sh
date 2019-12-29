# Build script for staticfiles Now deploy
echo "Start now_build_staticfiles.sh"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Installing missing python 3.6"
yum install -y https://centos6.iuscommunity.org/ius-release.rpm
yum install -y python36u

# Get pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.6 get-pip.py

# Install requirements
pip install -r requirements.txt

# Build static
export DJANGO_SETTINGS_MODULE=openx.settings.staticfiles_build
python3.6 manage.py collectstatic

echo "End now_build_staticfiles.sh"
