# scrapy_studies
Repo for scrapy studies
## For CHALLENGE.md
Parts 1,2,3 and 4 were done! Part 5 didn't have too much time.
### Answering few questions:
- **How long the full crawl takes**: 22 minutes, for part 4.
- **One thing that broke and how you found it**: during pipeline, image links were relative not absolute, so I concatenated with the root link.
- **One thing you'd do differently if the site had 1,000,000 books instead of 1000**: I would simply write a jsonl
### Logs after running check.py for part 4:
```
OK — 1000 books
Cheapest: An Abundance of Katherines
```
