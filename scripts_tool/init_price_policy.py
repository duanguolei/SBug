"""
code speace
@Time    : 2024/3/9 17:58
@Author  : 泪懿:dgl
@File    : init_price_policy.py
"""



# print(Fake.name(),Fake.email(),Fake.phone_number(),Fake.password())
import base
from web import models

def run():
    if not models.PricePolcy.objects.filter( category=1,
        title='个人免费版').exists():
        models.PricePolcy.objects.create(
            category=1,
            title='个人免费版',
            price=0,
            project_num=3,
            project_member=2,
            project_space=5,
            per_file_size=20,
                        )


if __name__ == '__main__':
    run()


