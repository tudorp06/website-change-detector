# website-change-detector
I love doing Python scripts and constantly learning new libraries, so I did a small website change detector (it's still a WIP) using path, difflib and requests. It fetches a website, turns the body content into SHA-256 digest, stores it in a locally declared file and then compares the stored SHA to the new one fetched. It displays the change diff.
