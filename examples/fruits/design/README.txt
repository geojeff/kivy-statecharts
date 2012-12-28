Assuming you are working in a virtualenv, to generate the statechart.png using
blockdiag,

pip install PIL

Check that freetype2 showed as available. If it did not show as available,
download it and install it (requires sudo, as freetype2 is a system lib), then,

pip uninstall PIL
pip install PIL

to install anew with freetype2.

pip install blockdiag

Now you should have blockdiag available on the command line, and can run:

blockdiag statechart.diag

which produces statechart.png

Learn how to write blockdiag definition files at blockdiag.com.
