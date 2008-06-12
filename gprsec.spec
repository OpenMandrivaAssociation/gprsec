# TODO: build also command line tool, automate configuration as defined below.

%define name		gprsec
%define realnam		GPRS_Easy_Connect
%define version		3.0.0
%define realver		300
%define release		%mkrel 1
%define Summary		GUI to simplify GPRS cellular data connection

Summary:		%{Summary}
Name:			%{name}
Version:		%{version}
Release:		%{release}
License:		GPL
Group:			Communications
URL:			http://www.gprsec.hu

Source0:		http://www.gprsec.hu/downloads/%{realnam}_%{realver}.tar.bz2
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot 
BuildArch:		noarch

Requires:		perl-Gtk2
Requires:		perl-Glib
Requires:		perl-Gtk2-TrayIcon
Requires:		perl-Gnome2-Canvas
Requires:		perl-Gnome2-VFS
Requires:		perl-Gnome2
Requires:		ppp

%description
GPRS Easy Connect is a graphical utility to simplify connecting to the internet
with a GPRS cellular phone.  Many phones are supported, and scripts to connect
to many worldwide GPRS providers are included.  You can also easily create your
own script to add new phones or new providers.  Connection statistics are also
included.

Connections to your phone can be via serial, irda, bluetooth, or USB.

* Usage note:
To use, make sure you have kernel module cdc_acm loaded (easiest is to add it
to /etc/modules), add user permissions after devices created by executing
chmod a+rw /dev/ttyACM0 && chmod a+rw /dev/ttyACM1, and after you connect to
run dhclient or similar.

%prep 
%setup -q -n %{realnam}_%{realver}

%build 
# no build, this is a perl script

%install
rm -rf %{buildroot}

# The spec does not use the binary installer provided in the package
# but the installation directives used by it from installer/Install.conf

install -D data/bin/%{name} %{buildroot}%{_bindir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -R data/share/%{name}/images %{buildroot}%{_datadir}/%{name}/
cp -R data/share/%{name}/themes %{buildroot}%{_datadir}
cp -R data/share/%{name}/languages %{buildroot}%{_datadir}/%{name}/
cp -R data/share/%{name}/sounds %{buildroot}%{_datadir}/%{name}/
cp -R data/share/%{name}/tools %{buildroot}%{_datadir}/%{name}/

# Creating menu entry


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=GPRS Easy Connect
Comment=%{Summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false (or true if needs=text)
Type=Application
Categories=GNOME;Settings;Networ;X-MandrivaLinux-System-Configuration-Networking;
EOF

# Create icons

install -d %buildroot/{%_miconsdir,%_iconsdir,%_liconsdir}
convert -resize 16x16 data/share/gprsec/images/icons/gprsec.png %buildroot/%_miconsdir/%name.png
convert -resize 32x32 data/share/gprsec/images/icons/gprsec.png %buildroot/%_iconsdir/%name.png
convert -resize 48x48 data/share/gprsec/images/icons/gprsec.png %buildroot/%_liconsdir/%name.png

%clean 
rm -rf %{buildroot} 

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root,0755) 
%doc data/share/gprsec/README data/share/gprsec/COPYING data/share/gprsec/AUTHORS data/share/gprsec/history data/share/gprsec/version
%doc documentation.html
%{_datadir}/applications/mandriva-%{name}.desktop
%{_bindir}/%name
%{_miconsdir}/%name.png
%{_iconsdir}/%name.png
%{_liconsdir}/%name.png
%{_datadir}/%{name}/*
%{_datadir}/themes/*

