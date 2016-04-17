###############################################################################

%define _smp_mflags -j1

###############################################################################

Summary:              A terminal multiplexer
Name:                 tmux
Version:              2.1
Release:              0%{?dist}
License:              ISC and BSD
Group:                Applications/System
URL:                  https://tmux.github.io

Source:               https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:        ncurses-devel libevent-devel >= 1.4.14b

###############################################################################

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

###############################################################################

%prep
%setup -q

%build
%configure
%{__make}  %{?_smp_mflags} LDFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{make_install} INSTALLBIN="install -pm 755" INSTALLMAN="install -pm 644"

%post
if [[ ! -f %{_sysconfdir}/shells ]] ; then
  echo "%{_bindir}/tmux" > %{_sysconfdir}/shells
else
  grep -q "^%{_bindir}/tmux$" %{_sysconfdir}/shells || echo "%{_bindir}/tmux" >> %{_sysconfdir}/shells
fi

%clean
%{__rm} -rf %{buildroot}

###############################################################################

%files
%defattr(-,root,root,-)
%doc CHANGES FAQ TODO examples/
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*

###############################################################################

%changelog
* Sat Jan 16 2016 Gleb Goncharov <ggoncharov@simtechdev.com> - 2.1-0
- Mouse-mode has been rewritten.
- 'default-terminal' is now a session option.
- The c0-* options for rate-limiting have been removed.
- 'copy-selection', 'append-selection', 'start-named-buffer' now understand
  an '-x' flag to prevent it exiting copying mode.
- 'select-pane' now understands '-P' to set window/pane background colours.
- 'renumber-windows' now understands windows which are unlinked.
- 'bind' now understands multiple key tables.  Allows for key-chaining.
- 'select-layout' understands '-o' to undo the last layout change.
- The environment is updated when switching sessions as well as attaching.
- 'select-pane' now understands '-M' for marking a pane.  This marked pane
  can then be used with commands which understand src-pane specifiers
  automatically.
- If a session/window target is prefixed with '=' then only an exact match
  is considered.
- 'move-window' understands '-a'.
- 'update-environment' understands '-E' when attach-session is used on an
  already attached client.
- 'show-environment' understands '-s' to output Bourne-compatible commands.
- New option: 'history-file' to save/restore command prompt history.
- Copy mode is exited if the history is cleared whilst in copy-mode.
- 'copy-mode' learned '-e' to exit copy-mode when scrolling to end.

