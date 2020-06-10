# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from yelp_scrapy.models import *


class YelpScrapyPipeline(object):
    def process_item(self, item, spider):
        Session = sessionmaker(bind=engine)
        session = Session()
        to_business = session.query(
            Business
        ).filter_by(
            source_url=item.get('source_url')
        ).first()
        if not to_business:
            to_business = Business(
                title=item.get('title'),
                source_url=item.get('source_url'),
                address=item.get('address'),
                telephone=item.get('telephone'),
                website=item.get('website'),
                timetable=item.get('timetable'),
                about=item.get('about'),
                images=item.get('images'),
                reviews=item.get('reviews'),
                add_time=item.get('add_time'),
            )
            session.add(to_business)
        else:
            to_business.update_version += 1
            to_business.update_time = func.now()

        to_category = session.query(
            Category
        ).filter_by(
            name=item.get('category')
        ).first()
        if not to_category:
            to_category = Category(
                name=item.get('category')
            )
            session.add(to_category)
        to_category.business.append(to_business)

        to_location = session.query(
            Location
        ).filter_by(
            name=item.get('location')
        ).first()
        if not to_location:
            to_location = Location(
                name=item.get('location')
            )
            session.add(to_location)
        to_location.business.append(to_business)
        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item
