# futbol
European football competition data

# How to install Apache Ignite

The `futbol` app uses Apache Ignite as its persistent data store. 

`docker pull apacheignite/ignite:latest`

`mkdir ignite_work` (run in the `futbol` base directory)

`docker run -d -v ${PWD}/ignite_work:/persistence -e IGNITE_WORK_DIR=/persistence apacheignite/ignite`
