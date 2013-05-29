from __future__ import division
import re
import os

class Summary(object):
	def split_content_to_sentences(self,content):
		content = content.replace("\n", ". ")
		return content.split(". ")
	
	def split_content_to_paragraphs(self,content):
		return content.split("\n\n")

	def sentences_intersection(self,sent1, sent2):

		s1 = set(sent1.split(" "))
		s2 = set(sent2.split(" "))

		if 0==(len(s1) + len(s2)):
			return 0

		return len(s1.intersection(s2))/((len(s1)+len(s2))/2)
	
	def format_sentence(self,sentence):
		sentence = re.sub(r'\W+','',sentence)
		return sentence
	
	def get_sentences_ranks(self, content):
		sentences = self.split_content_to_sentences(content)

		n = len(sentences)
		values = [[0 for x in xrange(n)] for x in xrange(n)]
		for i in range(0,n):
			for j in range(0,n):
				values[i][j] = self.sentences_intersection(sentences[i],sentences[j])

		sentences_dic = {}
		for i in range(0,n):
			score = 0
			for j in range(0,n):
				if i == j:
					continue
				score += values[i][j]
			sentences_dic[self.format_sentence(sentences[i])] = score
		return sentences_dic

	def get_best_sentence(self,paragraph,sentences_dic):

		sentences = self.split_content_to_sentences(paragraph)

		if len(sentences) < 2:
			return ""

		best_sentence = ""
		max_value = 0

		for s in sentences:
			strip_s = self.format_sentence(s)
			if strip_s:
				if sentences_dic[strip_s] > max_value:
					max_value = sentences_dic[strip_s]
					best_sentence = s
		return best_sentence
	
	def get_summary(self, title, content, sentences_dic):
		paragraphs = self.split_content_to_paragraphs(content)
		summary = []
		summary = { title: None, content: []}
		summary['title'] = title.strip()
		#summary.append("")

		summary['content'] = []
		
		for p in paragraphs:
			sentence = self.get_best_sentence(p, sentences_dic).strip()
			if sentence:
				summary['content'].append(sentence+'.')
		summary['content'] = ("\n\n").join(summary["content"])
		
		return summary

def main() :

	title = """Swayy is a beautiful new dashboard for discovering and curating online content"""
	file_dir = os.path.dirname(os.path.abspath(__file__))
	file_path = "../tests/test1.txt"
	file_abs_path = os.path.join(file_dir,file_path)
	
	with open(file_abs_path, 'r') as content_file:
		content = content_file.read()
	
	content = re.sub('[\r]', '', content)
		
	summary = Summary()
	sentences_dictionary = summary.get_sentences_ranks(content)
	summary_text = summary.get_summary(title,content,sentences_dictionary)

	print summary_text['title'] + "\n\n"
	print summary_text['content']

	print ""
	print "Original Length: %s" % (len(title)+len(content))
	print "Summary Length: %s" % len(summary_text['content']+summary_text['title'])
	print "Summary Ratio: %s" % (100 - (100*(len(summary_text['content']+summary_text['title'])/(len(title)+len(content)))))

if __name__ == '__main__':
	main()