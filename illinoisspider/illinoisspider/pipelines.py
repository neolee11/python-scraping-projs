# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import RC_Node
from .items import RC_Tree

class IllinoisspiderPipeline(object):
	def __init__(self):
		self.tree = RC_Tree()


	def write_to_file(self, ss):
		f = open("rc.xml", "a+")
		f.write(ss + '\n')
		f.close()


	def process_item(self, item, spider):
		node = RC_Node(item)
		parent = self.tree.get_parent(item['upper_ID'])
		self.tree.add_to_tree(node, parent)
		# self.write_to_file(repr(item))
	

	def close_spider(self, spider):
		self.tree.build_files()