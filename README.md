UnityLogCat
===========

Graphic tool using PySide for visualizing the logcat performance output from **Unity 3D** on **Android**.

Because I found that eyeballing the console spam looking for relevant changes was nearly impossible.

* Displays a graph for each of the performance values Unity logs.
* Graphs can be clicked on to highlight a specific point in time.
* All other unity-specific spew is directed into a text area for easy viewing.
* Most extreme value is highlighted in yellow (and cropped from the chart, as there are often obnoxious 1-frame spikes when the level loads that make the rest of the chart unreadable).
* Small connection indicator shows whether the phone is even outputting to logcat. (Darn flaky ADB.)


![](http://github.com/Ipsquiggle/UnityLogCat/raw/master/media/screenshot.png)

Todo
----

* Provide installation instructions (re: PySide)
* Get rid of hard-coded path to android SDK.
* Add coloring to the log based on log type (debug, info, etc.)
* Allow easy custom "targets" for any of the charts.
* Handle spikes more elegantly (e.g. highlight anything above some deviation, or something.)
* Synchronize selection across all charts, and possibly the output log as well.
