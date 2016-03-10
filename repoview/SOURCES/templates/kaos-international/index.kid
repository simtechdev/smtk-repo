<?xml version="1.0" encoding="utf-8"?>
<?python
import time
def ymd(stamp):
    return time.strftime('%d/%m/%Y', time.localtime(int(stamp)))
?>
<html xmlns:py="http://purl.org/kid/ns#">
<head>
  <title py:content="'RepoView KAOS: %s' % repo_data['title']"/>
  <link rel="stylesheet" href="layout/repostyle.css" type="text/css" />
  <link py:if="url is not None"
	  rel="alternate" type="application/rss+xml" title="RSS" href="latest-feed.xml" />
  <meta name="robots" content="index,follow" />
</head>
<body>
    <div class="levbar">
    <p class="pagetitle"><img width="160" height="160" src="layout/logo.png" /></p>
    </div>
    <div class="main">
        <p class="nav">Jump to letter: [
          <span class="letterlist">
            <a py:for="letter in repo_data['letters']"
              class="nlink"
              href="${'letter_%s.group.html' % letter.lower()}" py:content="letter"/>
          </span>]
        </p>
        
        <h3>Available Groups</h3>
        <ul class="pkglist">
          <li py:for="(name, filename, description, packages) in groups">
            <a href="${filename}" class="inpage"
                py:content="name"/>
          </li>
        </ul>

        <h3>Latest packages</h3>
        <ul class="pkglist">
          <li py:for="(name, filename, version, release, built) in latest">
            <em><span py:content="ymd(built)"/></em>:
            <a href="${filename}" class="inpage"
                py:content="'%s-%s-%s' % (name, version, release)"/>
          </li>
        </ul>
        
        <p class="footernote">
          <span py:content="'Listing generated: %s by' % ymd(time.time())"/>
          <a href="https://github.com/essentialkaos/repoview-kaos"
            class="repoview" py:content="'repoview-%s' % repo_data['my_version']"/>
        </p>
    </div>
</body>
</html>
