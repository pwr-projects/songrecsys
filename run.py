from pprint import pprint

from songrecsys import *

if __name__ == '__main__':
    config = ConfigMgr(CONFIG_DEFAULT_PATH)
    sp = SpotifyWrapper(config)
    
    sp.current_user_top_tracks(time_range='long_term')