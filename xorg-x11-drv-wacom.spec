%global tarball xf86-input-wacom
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

# Disable gitdate to build from a fixed release
#global gitdate 20111110
#global gitversion 12345689

Summary:    Xorg X11 wacom input driver
Name:       xorg-x11-drv-wacom
Version:    0.32.0
Release:    1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
URL:        http://www.x.org
License:    GPLv2+
Group:      User Interface/X Hardware Support
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?gitdate}
Source0: %{tarball}-%{gitdate}.tar.bz2
Source1: make-git-snapshot.sh
Source2: commitid
%else
Source0: http://prdownloads.sourceforge.net/linuxwacom/xf86-input-wacom-%{version}.tar.bz2
%endif

Patch004: 0004-RHEL6-Revert-error-checking.patch
Patch005: 0005-Grab-the-device-by-default.patch
Patch006: 0006-Define-the-required-bits-for-property-checking.patch

ExcludeArch: s390 s390x

BuildRequires: xorg-x11-server-sdk >= 1.10.99.902
BuildRequires: xorg-x11-util-macros >= 1.3.0
BuildRequires: libX11-devel libXi-devel libXrandr-devel libXinerama-devel
BuildRequires: autoconf automake libtool pkgconfig
BuildRequires: libudev-devel

Requires:  Xorg %(xserver-sdk-abi-requires ansic)
Requires:  Xorg %(xserver-sdk-abi-requires xinput)
Requires:  hal udev libudev
Requires:  libX11 libXi libXrandr libXinerama


Provides:  linuxwacom = %{version}-%{release}
Obsoletes: linuxwacom <= 0.8.4.3

%description
X.Org X11 wacom input driver for Wacom tablets.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
%patch004 -p1
%patch005 -p1
%patch006 -p1

%build
autoreconf --force -v --install || exit 1
# empty conf dir to force HAL
%configure --disable-static --disable-silent-rules \
           --with-xorg-conf-dir='' \
           --without-systemd-unit-dir \
           --without-udev-rules-dir
make %{_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

install -d $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty
install -m 0644 ${RPM_BUILD_ROOT}%{_datadir}/hal/fdi/policy/20thirdparty/wacom.fdi $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty/10-wacom.fdi
rm ${RPM_BUILD_ROOT}%{_datadir}/hal/fdi/policy/20thirdparty/wacom.fdi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS README GPL
%if !0%{?gitdate}
# ChangeLog is autogenerated by make dist, we don't run it from git builds
%doc ChangeLog
%endif
%{driverdir}/wacom_drv.so
%{_mandir}/man4/wacom.4*
%{_mandir}/man1/xsetwacom.1*
%{_datadir}/hal/fdi/policy/20thirdparty/10-wacom.fdi
%{_bindir}/xsetwacom
%{_bindir}/isdv4-serial-inputattach

%package devel
Summary:    Xorg X11 wacom input driver development package
Group:      Development/Libraries

Requires: xorg-x11-server-devel >= 1.7.0
Requires: pkgconfig

%description devel
X.Org X11 wacom input driver development files.

%files devel
%defattr(-,root,root,-)
%doc GPL
%{_libdir}/pkgconfig/xorg-wacom.pc
%{_includedir}/xorg/Xwacom.h
%{_includedir}/xorg/wacom-properties.h
%{_includedir}/xorg/wacom-util.h
%{_includedir}/xorg/isdv4.h
%{_bindir}/isdv4-serial-debugger

%changelog
* Wed Nov 25 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.32.0-1
- wacom 0.32.0 (#1248619)

* Wed Nov 11 2015 Adam Jackson <ajax@redhat.com> 0.23.0-5
- Rebuild for server 1.17

* Mon Jun 02 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.23.0-4
- Disable action property error checking to ignore invalid values from g-s-d
  (#1077478)

* Thu May 08 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.23.0-3
- Merge RHEL7 extra patches, add RHEL6 compat patch to enable INPUT_PROP
  checking
- Grab the event device by default for backwards-compat (#1077478)

* Wed May 07 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.23.0-2
- Don't fail on invalid action properties, just ignore them. g-s-d can't
  handle that, see #1095019. (#1077478)
- Drop all now unused patches

* Wed Apr 23 2014 Adam Jackson <ajax@redhat.com> 0.23.0-1
- wacom 0.23.0

* Mon Jul 01 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.16.1-4
- Add support for more special symbols to xsetwacom (#920385)

* Thu Nov 01 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.16.1-3
- Fix {?dist} tag (#871448)

* Tue Oct 09 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.16.1-2
- Fix crash for xorg.conf devices with same device node (#862939)
- Fix spurious cursor jump when using I5 express keys (#859851)

* Mon Aug 27 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.16.1-1
- Merge from F18 (#835226)

* Wed May 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-6
- Add PTK-540WL (Intuos4 WL) to fdi (#818038)

* Thu Mar 22 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-5
- Fix Coverty complaints (#802385)

* Fri Mar 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-4
- Export the current tool ID through the serial ID property.

* Fri Feb 17 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-3
- Initialize the right number of button properties.
- Allow -1 as pressure threshod reset value. 
- Remove now unused patches

* Mon Feb 13 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-2
- Re-add hal as Requires (related #752642)
- Update util-macros requirement to 1.8, that's really what we need.

* Mon Feb 13 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-1
- Rebase to 0.13.0 (#752642)

* Tue Sep 20 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-14
- Fix typo in man page (#641759)

* Tue Jul 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-13
- Fix crashes on startup if PreInit fails for a device (related #713769)

* Wed Jul 13 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-12
- Fix minor memleak in xsetwacom (#717213)
- Disable silent rules on build

* Wed Jul 06 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-11
- Allow for Twinview Resolution 0 values on TV_NONE (#711619)
- Fix cintiq calibration issues (#675672)

* Wed Jun 29 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-10
- Update to support ABI 12 (#713769)

* Fri Apr 08 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-9
- Fix button mapping in xsetwacom to allow for last button to be mapped 
  (related #620957)

* Wed Apr 06 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-8
- Add support for Cintiq 21UX2 (#620957)

* Thu Feb 03 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-8
- Several patches related to bug #624560
  - xsetwacom: remove core keyword parsing, has no effect
  - fix button map handling in xsetwacom
  - add more keywords and special characters
  - twinview and calibration fixes

* Thu Oct 14 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-7
- wacom-0.10.5-xsetwacom-add-super-and-hyper-to-modifiers.patch: parse Hyper
  and Super as modifiers.
- wacom-0.10.5-xsetwacom-fix-strjoinsplit.patch: fix parameter advancement.
- A list of patches to improve TwinView configuration (#624560).

* Wed Jul 28 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-6
- wacom-0.10.5-keycodes-not-keysyms.patch: load keycodes into the driver,
  not keysyms. Avoids server hangs when XkbGetCoreMap() allocs in signal
  handler (#616653)
- wacom-0.10.5-scroll-wheel-zoom.patch: zoom with wheel, not ctrl+/- since
  the latter is now layout-dependent.

* Mon Jun 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-5
- wacom-0.10.5-wheel-events.patch: don't convert the wheel events to scroll
  events for anything but the pad (#593948)

* Thu Jun 10 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-4
- Remove wacom-0.10.5-axis-mode.patch: this is an X server bug (#594523)
- wacom-0.10.5-relative-pressure.patch: subtract old pressure from new
  pressue values to get a relative value (#597932)
- wacom-0.10.05-xsetwacom-man-page.patch: add xsetwacom man page (#598312)

* Wed May 26 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-3
- wacom-0.10.5-axis-mode.patch: don't merge OutOfProximity flags to axis
  mode (#594523)

* Thu Apr 22 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-2
- wacom-0.10.5-linuwacom-man-page.patch: drop reference to linuxwacom from
  man page (#584588)
- wacom-0.10.5-pad-scrolling.patch: force relative mode for pad (#584589)
- wacom-0.10.5-tpcbutton-on.patch: enable TPCButton for ISDV4 devices
  (#584597)

* Fri Mar 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.5-1
- wacom 0.10.5 (#575014)
- wacom-0.10.4-license-fix.patch: Drop, upstream.

* Fri Feb 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-2
- wacom-0.10.4-license-fix.patch: fix license copy/paste errors. Patch from
  upstream (#566622)

* Wed Feb 03 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.10.4-1
- wacom 0.10.4
- Update sources to point to sourceforge.
- Install the upstream fdi file instead of our custom one.
- Update Requires and BuildRequires for xsetwacom.

* Mon Nov 23 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.1-2
- 10-linuxwacom.fdi: squash extra entry for bluetooth tablet into general
  Wacom match. 
- 10-linuxwacom.fdi: remove info.parent condition for N-Trig (#538036)

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.1-1
- wacom 0.10.1
- Remove unnecessary 'find' directive, changed upstream.
- Add GPL document
- Install 10-wacom.fdi file.
- Provides: linuxwacom

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-4
- BuildRequires xorg-x11-util-macros 1.3.0

* Thu Nov 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-3
- Use smp_mflags when building.

* Wed Nov 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-2
- Obsolete linuxwacom, don't Conflict with it.
- Remove trailing dot from summary (rpmlint warning).
- Remove spurious executable bits from source files (rpmlint warning).
- Add AUTHORS, ChangeLog, README to doc

* Mon Oct 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-1
- Initial import

