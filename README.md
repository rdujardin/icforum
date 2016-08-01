# icforum
Forum Infinite Connection

## technology
 * Written in Python 3.5.x with the framework Django.
 * Deployment with Nginx and USWGI.
 * Responsive design with Bootstrap 3 and jQuery.
 * Versioned with Git.

## main goals
 * bases of a forum, organized with tags instead of categories (allowing to filter directly instead of browsing) : user and group system with authentication and permissions system on groups, topics (creating, viewing with pagination, editing, deleting), messages (posting, editing, deleting)
 * allow complex messages with highlighted code snippets, youtube videos, images, formatting ; all with a WYSIWIG editor (still allowing to modify manually the source code) ; all with security (prevent XSS attacks..)
 * administration panel
 * readable API allowing to make future external tools (mobile app ? ..)
 * possibility to backup/restore the database manually and from a cron
 * modern responsive design, adapted to every media (large screen, tablet, mobile, ..) ; maybe allow theming..
 * SEO
 * deployment : MySQL database, nginx/uwsgi with git pulling and two versions preprod and prod
 * then all the little extra features we want : clipboard link, quoting, profiles and avatars, etc.
