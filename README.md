## Lineup Scraper

Python3 script to track band announcements for some selected European music 
festivals. 

Produces csv output, in the form of a table with festivals as columns, bands
as rows, presence in the form of a 0-1 matrix.

           | festival 1    | festival 2    | festival 3    | ...
    band 1  | 0             | 1             | 0             | ...
    band 2  | 1             | 0             | 1             | ...
    ...     |               |               |               | ...

Dependencies are some libraries for css selectors and json handling, wget
module, but also command line wget, since some sites do not allow scraping
and custom user agent is needed, which the library does not seem to support.

Customization/move to different festivals is easy, just edit the dictionaries
in the "festival" list; enough samples are provided in the committed code, 
but in short essential info are lineup URL and a **unique** css selector path
that will get only band names (or a json object walker, in case the festival
page is generated dynamically from a json response). A *normalizer* for the 
band names is provided, may need to be extended.

Script is meant to be run manually, or cron'd with a few days/weeks interlude;
it's a good idea not to abuse it, e.g. I ran into 1 blacklist incident while 
testing.

## Companion scripts

There are a couple of companion scripts that work on the assumption that there
exists a second file, a preference file, which is a similar table with this 
structure, where the list of bands should be the output of the previous script.

           | person 1  | person 2  | person 3  | ...
    band 1  | 1         | 1         | 1         | ...
    band 2  | 0         | 0         | 0         | ...
    ...     |           |           |           | ...`

This is a file you distributed manually to the group of people you are planning
to travel to a festival with (if you are planning to go in a group) and 
represents the interest of the group for the bands announced. 

Since all of this is not integrated in a single software, but is a bunch of 
CSVs, and the band list is in alphabetical order for convenience, the problem
is that if you distribute one version of the file, then new announcements are
made in the following weeks, updating the preferences file with the band list
in the new presences file without losing existing preferences can be 
accomplished with the merge_prefs script.

Finally, once the preferences are finalized, you can obtain the line up of the
festivals in order of preferences in your group, instead of relying on the 
festival organizers' selection of headliners :)