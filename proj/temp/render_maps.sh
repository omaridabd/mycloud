cd /home/user/mycloud/proj
names=$(python3 -c "import sys;sys.path.insert(0,'graphics');from map_specs import SPECS;print(' '.join(s['name'] for s in SPECS))")
echo $names | tr ' ' '\n' | xargs -P 3 -I{} python3 graphics/maps.py {}
echo ALLDONE
