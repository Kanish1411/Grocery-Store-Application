To run the backend

cd /backend/
pip install -r req.txt
python app.py

To run frontend (on a new terminal)

cd /frontend
npm run dev

if Redis server is needed 
run redis server before starting backednd or frontend with command on a linux terminal

sudo apt update
sudo apt install redis-server
sudo service redis-server start
