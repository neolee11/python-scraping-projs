# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import uuid
import re
from io import BytesIO
from lxml import etree
from collections import OrderedDict


class XMLNamespaces:
   xs = 'http://www.w3.org/2001/XMLSchema'
   a = 'http://www.w3.org/2005/08/addressing'


class IllinoisspiderItem(scrapy.Item):
	# define the fields for your item here like:
	title = scrapy.Field()
	ID = scrapy.Field()
	upper_ID = scrapy.Field()
	content = scrapy.Field()
	index = scrapy.Field()
	caption = scrapy.Field()
	pass


class RC_Node():
	def __init__(self, item=None):
		if item is not None:
			self.ID = item['ID']
			self.upper_ID = item['upper_ID']
			self.title = item['title']
			self.content = item['content']
			self.index = item['index']
			self.caption = item['caption']
		else:
			self.ID = '1'
			self.upper_ID = '1'
			self.title = '1'
			self.content = '1'
			self.index = '1'
			self.caption = '1'
		self.next = []


	def __str__(self, level=0):
		ret = "\t"*level+repr(self.ID + '******' + self.content + '******' + str(self.index))+"\n"

		f = open("rc.xml", "a+")
		f.write(ret)
		f.close()

		for child in self.next:
			ret += child.__str__(level+1)
		return ret


	def __repr__(self):
		return '<tree node representation>'


	def get_rev_children(self):
		children = self.next[:]
		children.reverse()
		return children     


class RC_Tree():
	def __init__(self):
		self.root = RC_Node()
		self.path_calculate = {}


	def get_parent(self, upperID):
		visited, stack = set(), [self.root]
		while stack:
			vertex = stack.pop()
			if vertex.ID == upperID:
				del stack[:]
				visited.clear()
				return vertex
			if vertex not in visited:
				visited.add(vertex)
				stack.extend(set(vertex.next) - visited)
		return self.root


	def add_to_tree(self, node, parent):
		node.parent = parent
		parent.next.append(node)
		parent.next = sorted(parent.next, key=lambda child: child.index)

	
	def build_heading(self):
		today = datetime.date.today()
		
		# <Document> attribute
		xs = 'http://www.w3.org/2001/XMLSchema'
		xmlns = 'http://www.jpmorgan.com/olo'
		root = etree.Element("{" + xmlns + "}Document", id=str(uuid.uuid4()), nsmap={'xs':xs, None:xmlns})
		source = etree.Element('Source')
		source.text = 'Vermont Securities Regulations'
		reference = etree.Element('Reference')
		reference.text = 'http://www.dfr.vermont.gov/reg-bul-ord/vermont-securities-regulations'
		version = etree.Element('Version')
		version.text = today.strftime('%B %d, %Y')
		root.append(source)
		root.append(reference)
		root.append(version)

		return root


	def traverse(self, node, path, level):
		if re.match(r'<p>\s*V\.S\.R\.', node.title) is not None:
			node.title = re.search(r'\d+-\d+', node.content).group(0)
		elif re.match(r'(<p>)\s*\([a-z]+\)', node.title) is not None:
			level = 5
		elif re.match(r'<p>\s*\(\d+\)', node.title) is not None:
			level = 6
		elif re.match(r'<p>\s*\([A-Z]\)', node.title) is not None:
			level = 7
		elif re.match(r'(<c>)\s*\(x{0,3}(ix|iv|v?i{0,3})\)', node.title) is not None:
			level = 8
		
		node.title = self.clean_content(node.title)

		if node.title != 'Notes':
			if path + '/' + node.title in self.path_calculate:
				self.path_calculate[path + '/' + node.title] = self.path_calculate[path + '/' + node.title] + 1
				node.title = node.title + '_' + str(self.path_calculate[path + '/' + node.title])
			else:
				self.path_calculate[path + '/' + node.title] = 0


		reference_content = etree.Element('ReferencedContent', OrderedDict([("id", node.ID), ("path", path + '/' + node.title), ("level", str(level))]))
		content = etree.SubElement(reference_content, 'Content')
		content = self.extract_table_in_content(node.title, content, node.content, node.caption)

		if len(node.next) != 0:
			for child in node.next:
				child_reference_content = self.traverse(child, path + '/' + node.title, level + 1)    
				content.append(child_reference_content)

		return reference_content


	def extract_table_in_content(self, title, content_tag, content, caption):
		pre = etree.Element('pre')

		content = self.clean_content(content)

		if re.search(r'\w+', content) is not None:
			pre.text = content
			content_tag.append(pre)
		else:
			pre.text = caption
			content_tag.append(pre)

		return content_tag


	def build_files(self):
		for child in self.root.next:
			today = datetime.date.today()
			path, level = '/us/vermontsecuritiesregulations', 2
			ret = self.build_heading()
			ret2 = self.traverse(child, path, level)
			ret.append(ret2)
			ret = etree.tostring(ret, pretty_print=True, xml_declaration=True, encoding='utf-8')
			self.write_to_file2(ret, today)


	def write_to_file(self, ss):
		f = open("rc.xml", "a+")
		f.write(ss.ID + '*****' + ss.title + '*****' + ss.content + '*****' + str(ss.index))
		f.write('\n')
		f.close()


	def write_to_file2(self, content, today):
		try:
			date = today.strftime('%m-%d-%Y')
			f = open('VermontSecuritiesRegulations -' + date +  '.rc.xml', "ab+")
			f.write(content)
			f.close()
		except Exception as e:
			print (content)
			print (str(e))


	def traverse2(self):
		stack = [self.root]
		while stack:
			cur_node = stack[0]
			self.write_to_file(cur_node)
			stack = stack[1:]      
			for child in cur_node.get_rev_children():
				stack.insert(0, child)

		# print (self.root)
	
	def clean_content(self, content):
		# clean <c> tag
		cleanr = re.compile('<c>')
		content = re.sub(cleanr, '\n', content)
		cleanr = re.compile('<d>')
		content = re.sub(cleanr, '\n', content)
		cleanr = re.compile('</p>\s*<p>')
		content = re.sub(cleanr, '\n', content)
		cleanr = re.compile('<p>')
		content = re.sub(cleanr, '\n', content)
		cleanr = re.compile('</p>')
		content = re.sub(cleanr, '', content)


		# if new line exists at start and end, ignore them
		cleanr = re.compile('^\s*')
		content = re.sub(cleanr, '', content)
		cleanr = re.compile('\s*$')
		content = re.sub(cleanr, '', content)

		return content.strip()