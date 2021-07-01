"""A video player class."""

from video_library import VideoLibrary
import random as rnd


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playlists = dict()
        self.playing = ""
        self.pause = ""
        self.all_videos = []
        self.plname = []
        self.flg = dict()
        self.vdoflg = dict()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        x = self._video_library.get_all_videos()
        for i in x:
            if i.video_id not in self.flg.keys():
                j = "{} ({}) [{}]".format(i.title, i.video_id, " ".join(i.tags))
                if j not in self.all_videos:
                    self.all_videos.append(j)
            else:
                j = "{} ({}) [{}] - FLAGGED (reason: {})".format(i.title, i.video_id, " ".join(i.tags), self.flg[i.video_id])
                if j not in self.all_videos:
                    self.all_videos.append(j)

        self.all_videos.sort()
        for i in self.all_videos:
            print(i)

    def play_video(self, video_id):
        if video_id not in self.flg.keys():
            n = self._video_library.get_video(video_id)
            if n:
                if self.playing != "":
                    print("Stopping video: {}".format(self.playing.title))
                    print("Playing video: {}".format(n.title))
                    self.playing = n
                    self.pause = ""
                else:
                    print("Playing video: {}".format(n.title))
                    self.playing = n
                    self.pause = ""
            else:
                print("Cannot play video: Video does not exist")
        else:
            print("Cannot play video: Video is currently flagged (reason: {})".format(self.flg[video_id]))

    def stop_video(self):
        """Stops the current video."""
        if self.playing:
            print("Stopping video: {}".format(self.playing.title))
            self.playing = ""
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        x = self._video_library.get_all_videos()
        z = []
        for i in x:
            if i.video_id not in self.flg.keys():
                z.append(i.video_id)
        if z:
            self.play_video(rnd.choice(z))
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self.playing:
            if not self.pause:
                print("Pausing video: {}".format(self.playing.title))
                self.pause = self.playing.title
            else:
                print("Video already paused: {}".format(self.pause))
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.pause:
            print("Continuing video: {}".format(self.pause))
            self.pause = ""
        elif not self.playing:
            print("Cannot continue video: No video is currently playing")
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        if not self.playing:
            print("No video is currently playing")
        else:
            if self.pause != "":
                print("Currently playing: {} ({}) [{}] - PAUSED".format(self.playing.title, self.playing.video_id,
                                                                        " ".join(self.playing.tags)))
            else:
                print("Currently playing: {} ({}) [{}]".format(self.playing.title, self.playing.video_id,
                                                               " ".join(self.playing.tags)))

    def create_playlist(self, playlist_name):
        if playlist_name.lower() not in self.playlists.keys():
            self.playlists[playlist_name.lower()] = []
            print("Successfully created new playlist: {}".format(playlist_name))
            self.plname.append(playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        if video_id not in self.flg.keys():
            vdo = self._video_library.get_video(video_id)
            if playlist_name.lower() in self.playlists.keys():
                if vdo != None:
                    v = "{} ({}) [{}]".format(vdo.title, video_id, " ".join(vdo.tags))
                    if v not in self.playlists[playlist_name.lower()]:
                        self.playlists[playlist_name.lower()].append(v)
                        print("Added video to {}: {}".format(playlist_name, vdo.title))
                    else:
                        print("Cannot add video to {}: Video already added".format(playlist_name))
                else:
                    print("Cannot add video to {}: Video does not exist".format(playlist_name))
            else:
                print("Cannot add video to {}: Playlist does not exist".format(playlist_name))
        else:
            print("Cannot add video to {}: Video is currently flagged (reason: {})".format(playlist_name, self.flg[video_id]))

    def show_all_playlists(self):
        """Display all playlists."""
        if self.playlists.keys():
            print("Showing all playlists:")
            key = sorted(list(self.playlists.keys()))
            for i in key:
                for j in self.plname:
                    if i.lower() == j.lower():
                        print("{}".format(j))
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        if playlist_name.lower() in self.playlists.keys():
            for i in self.flg.keys():
                j = self._video_library.get_video(i)
                self.vdoflg[i] = "{} ({}) [{}]".format(j.title, j.video_id," ".join(j.tags))
            print("Showing playlist: {}".format(playlist_name))
            if self.playlists[playlist_name.lower()]:
                for i in self.playlists[playlist_name.lower()]:
                    if i in self.vdoflg.values():
                        vid = i.split("(")[1]
                        vid = vid.split(")")[0]
                        print("{} - FLAGGED (reason: {})".format(i,self.flg[vid]))
                    else:
                        print("{}".format(i))
            else:
                print("No videos here yet")
        else:
            print("Cannot show playlist {}: Playlist does not exist".format(playlist_name))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.lower() in self.playlists.keys():
            vdo = self._video_library.get_video(video_id)
            if vdo:
                vdo2 = "{} ({}) [{}]".format(vdo.title, video_id, " ".join(vdo.tags))
                if vdo2 in self.playlists[playlist_name.lower()]:
                    self.playlists[playlist_name.lower()].remove(vdo2)
                    print("Removed video from {}: {}".format(playlist_name, vdo.title))
                else:
                    print("Cannot remove video from {}: Video is not in playlist".format(playlist_name))
            else:
                print("Cannot remove video from {}: Video does not exist".format(playlist_name))
        else:
            print("Cannot remove video from {}: Playlist does not exist".format(playlist_name))

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            print("Successfully removed all videos from {}".format(playlist_name))
            self.playlists[playlist_name.lower()] = []
        else:
            print("Cannot clear playlist {}: Playlist does not exist".format(playlist_name))

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            print("Deleted playlist: {}".format(playlist_name))
            x = self.playlists.pop(playlist_name.lower())
        else:
            print("Cannot delete playlist {}: Playlist does not exist".format(playlist_name))

    def search_videos(self, search_term):
        n = self._video_library.get_all_videos()
        se = []
        for i in n:
            for j in search_term.split(" "):
                if j.lower() in i.title.lower():
                    if i.video_id not in self.flg.keys():
                        se.append("{} ({}) [{}]".format(i.title, i.video_id, " ".join(i.tags)))
        if se:
            ss = set(se)
            se = list(ss)
            se = sorted(se)
            n=1
            print("Here are the results for {}:".format(search_term))
            for i in se:
                print(str(n)+")", i)
                n+=1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            try:
                inp = int(input())
                vdo = se[inp-1]
                vdo = list(vdo.split("("))
                vdo = vdo[0]
                print("Playing video: {}".format(vdo[:-1]))
                self.playing = vdo
                self.pause = ""
            except:
                pass
        else:
            print("No search results for {}".format(search_term))



    def search_videos_tag(self, video_tag):
        se = []
        n = self._video_library.get_all_videos()
        for i in n:
            if video_tag in i.tags and video_tag not in se:
                if i.video_id not in self.flg.keys():
                    se.append("{} ({}) [{}]".format(i.title, i.video_id, " ".join(i.tags)))
        if se:
            se = set(se)
            se = list(se)
            se.sort()
            print("Here are the results for {}:".format(video_tag))
            j = 1
            for i in se:
                print(str(j) + ")", i)
                j += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            try:
                inp = int(input())
                vdo = se[inp - 1]
                vdo = list(vdo.split("("))
                vdo = vdo[0]
                print("Playing video: {}".format(vdo[:-1]))
                self.playing = vdo
                self.pause = ""
            except:
                pass
        else:
            print("No search results for {}".format(video_tag))

    def flag_video(self, video_id, flag_reason=""):
        try:
            if self.playing:
                if self.playing.video_id == video_id:
                    print("Stopping video: {}".format(self.playing.title))
                    self.playing=""
                    self.pause=""
            if flag_reason=="":
                flag_reason = "Not supplied"
            if video_id not in self.flg.keys():
                print("Successfully flagged video: {} (reason: {})".format(self._video_library.get_video(video_id).title, flag_reason))
                self.flg[video_id] = flag_reason
            else:
                print("Cannot flag video: Video is already flagged")

        except:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        if self._video_library.get_video(video_id) != None:
           if video_id in self.flg.keys():
               print("Successfully removed flag from video: {}".format(self._video_library.get_video(video_id).title))
               x = self.flg.pop(video_id)
               if video_id in self.vdoflg.keys():
                   x = self.vdoflg.pop(video_id)
           else:
               print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")
