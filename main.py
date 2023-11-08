import argparse
from DataAugment import DataAugment

if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument('--task', type=str, default='cpr', help='task crawler [ppi, ade, cpr]')
    parser.add_argument('--domain', type=str, default='domain/domain-cpr-pubmed-id.csv', help='domain pubmed id task path .csv')
    parser.add_argument('--column_name', type=str, default='pubmed_id', help='the name in csv of rol pubmed ids')
    parser.add_argument('--level', type=int, default=3, help='max depth level to crawl similar link')
    parser.add_argument('--limit', type=int, default=100000, help='max crawl abstract')
    parser.add_argument('--batch_size', type=int, default=64, help='batch size')
    parser.add_argument('--output', type=str, default='cpr-abstract-augument.csv', help='output file csv data augment') 
    args = parser.parse_args()
    crawler = DataAugment(
        task= args.task, 
        domain=args.domain,
        pubmed_id_name_colums=args.column_name,
        max_level=args.level,
        crawl_limit=args.limit,
        batch_size=args.batch_size,
        output=args.output
    )
    crawler.run()
