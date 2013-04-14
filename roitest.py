import roi

index = roi.ROIIndexer('roi.cfg')
index.fullIndex('/optimise/source')
index.search('you', 'en_GB.po','de.po')
