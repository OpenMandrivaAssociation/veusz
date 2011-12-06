Name:           veusz
Version:        1.14
Release:        1
# The entire source code is GPLv2+ except helpers/src/_nc_cntr.c which is Python
License:        GPLv2+ and Python license
Summary:        GUI scientific plotting package
Url:            http://home.gna.org/veusz/
Group:          Sciences/Mathematics
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
BuildRequires:  python-numpy-devel
BuildRequires:  python-qt4-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sip
Requires:       python-numpy
Requires:       python-qt4
Requires:	python-%{name} = %{version}-%{release}
%{py_requires}

%description
Veusz is a scientific plotting package, designed to create
publication-ready Postscript/PDF/SVG output. It features GUI,
command-line, and scripting interfaces. Graphs are constructed from
widgets, allowing complex layouts to be designed. Veusz supports
plotting functions, data with errors, keys, labels, stacked plots,
multiple plots, contours, shapes and fitting data.

%package -n python-%{name}
Summary:        Python libraries for %{name}

%description -n python-%{name}
Veusz is a scientific plotting package, designed to create
publication-ready Postscript/PDF/SVG output. It features GUI,
command-line, and scripting interfaces. Graphs are constructed from
widgets, allowing complex layouts to be designed. Veusz supports
plotting functions, data with errors, keys, labels, stacked plots,
multiple plots, contours, shapes and fitting data.


%prep
%setup -q
find -name \*~ -delete

# change path of where to lookup bitmaps
# this is so we can move the icons out of the python directory
# and into /usr/share/pixmaps/veusz
sed -i "/imagedir =/c\\imagedir = '%{_datadir}/pixmaps/veusz'" \
        %{_builddir}/veusz-%{version}/utils/action.py

# change path of where to look for COPYING - should be docdir
sed -i "/f =/s+utils.veuszDirectory+'%{_docdir}/%{name}'+" \
        %{_builddir}/veusz-%{version}/dialogs/aboutdialog.py

%build
CFLAGS="%{optflags}"
python setup.py build
xz -k Documents/veusz*.1

%install
python setup.py install -O1 --skip-build --prefix="%{_prefix}" \
                                              --root=%{buildroot}

# install desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Veusz
Comment=Open .vsz scientific plotting files
GenericName=Veusz scientific plotting
Exec=veusz %F
StartupNotify=true
Terminal=false
Type=Application
Icon=veusz
Categories=GTK;GNOME;Education;Graphics;3DGraphics;X-Science,X-DataVisualization;
Encoding=UTF-8
MimeType=application/x-veusz;
EOF

# file to register .vsz mimetype
install -d %{buildroot}%{_datadir}/mime/packages/
cat > %{buildroot}%{_datadir}/mime/packages/%{name}.xml << EOF
<?xml version='1.0'?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="application/x-veusz">
    <comment>Veusz saved graph</comment>
    <glob pattern="*.vsz"/>
    <magic priority="50">
        <match type="string" value="# Veusz saved document" offset="0"/>
    </magic>
  </mime-type>
</mime-info>
EOF

# move icon files to /usr/share/pixmaps/veusz
# symlink main veusz icon also into pixmaps (for desktop file)
install -d %{buildroot}%{_datadir}/pixmaps/veusz
mv %{buildroot}%{python_sitearch}/veusz/windows/icons/*.png \
        %{buildroot}%{_datadir}/pixmaps/veusz
mv %{buildroot}%{python_sitearch}/veusz/windows/icons/*.svg \
        %{buildroot}%{_datadir}/pixmaps/veusz
ln -s veusz/veusz_48.png %{buildroot}%{_datadir}/pixmaps/veusz.png

# Mark some scripts as executable.
# This isn't really needed, but Veusz includes shebangs in scripts
# so that they can be run when not installed.
# Do this so that the scripts don't need modification.
chmod +x %{buildroot}%{python_sitearch}/veusz/veusz_main.py
chmod +x %{buildroot}%{python_sitearch}/veusz/veusz_listen.py

# install man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 Documents/veusz.1.xz Documents/veusz_listen.1.xz \
        %{buildroot}%{_mandir}/man1

%files
%doc README AUTHORS COPYING ChangeLog
%doc examples/
%doc Documents/manual.html
%doc Documents/manimages/
%{_bindir}/veusz
%{_bindir}/veusz_listen
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}/
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/*

%files -n python-%{name}
%doc README AUTHORS COPYING ChangeLog
%{python_sitearch}/%{name}
%{python_sitearch}/%{name}-%{version}-py%{py_ver}.egg-info
