-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: ProjectDB
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `API_Details`
--

DROP TABLE IF EXISTS `API_Details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `API_Details` (
  `APIName` varchar(255) DEFAULT NULL,
  `Tags` varchar(255) DEFAULT NULL,
  `Context` varchar(255) DEFAULT NULL,
  `Resources` varchar(255) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `API_Details`
--

LOCK TABLES `API_Details` WRITE;
/*!40000 ALTER TABLE `API_Details` DISABLE KEYS */;
INSERT INTO `API_Details` VALUES ('Amazon S3 ','[\"Storage\",\"Cloud\"]','/amazon-s3/1.0.0','[/store, /retrieve-data, /search]','Since 2006 Amazon Web Services has been offering web services commonly known as cloud computing. AWS Provides a reliable, low cost infrastructure platform that powers hundreds of thousands of businesses. Amazon S3 API, the Simple Storage Service provides '),('Bing','[\"search\",\"Machine Learning\"]','/bing/1.0.0','[/web-search, /search-history, /bookmarks]','The Bing API provides an experience similar to Bing.com/search by returning search results that Bing determines are relevant to a user\'s query. The results include Web pages and may also include images, videos, and more. Free trial keys are available here'),('Booking','[\"Travel\"]','/booking/1.0.0','[/locations, /currencies, /properties]','Booking API helps to query rooms, price, facilities, policities, etc information from many hotels around the world as on official site.'),('Breaking News','[\"Finance\"]','/breaking-news/1.0.0','[/getTopNews, /news, /getCompanyDetails]','MyAllies News delivers news from across the globe and information on the latest breaking business and financial news. Breaking news from around the globe as and when it happens using our complex web crawling technologies, information and big announcements'),('Currency Converter','[\"Finance\",\"Currency\"]','/currency-converter/1.0.0','[/rates, /available-currencies, /convert]','Provides exchange rates based on the official banks data. It returns the list of available currencies. '),('Domainr','[\"Business\"]','/domainr/1.0.0','[/search, /status, /register]','Instant domain search. Responds with search suggestions related to the query. Check domain availability. Responds with an HTTP redirect to a supporting registrar.'),('Fiz places','[\"Travel\"]','/fizplaces/1.0.0','[/lists, /places]','High quality, curated content on top places around the world including: top hotspots, landmarks, restaurants, POIs, museums, parks etc etc. Places are scored using Fiz unique algorithm, to determine \'relevance\' and \'popularity\'. The Lite endpoint may be u'),('Flickr','[\"Photos\",\"Video\"]','/flickr/1.0.0','[/service, /upload, /retrieve]','The Flickr API can be used to retrieve photos from the Flickr photo sharing service using a variety of feeds - public photos and videos, favorites, friends, group pools, discussions, and more. The API can also be used to upload photos and video.The Flickr'),('Foursquare','[\"Photos\",\"Social\",\"Search\",\"Mapping\",\"Mobile\"]','/foursquare/1.0.0','[/get-information, /search, /locate]','The Foursquare Places API provides location based experiences with diverse information about venues, users, photos, and check-ins. The API supports real time access to places, Snap-to-Place that assigns users to specific locations, and Geo-tag. Additional'),('GooglePlaces','[\"Mapping\"]','/GooglePlacesdimasV1/1.0.0','[/addPlace, /getImageURL, /getNearbyPlaces, /getPlaceDetails, /searchPlacesByText]','Connect to the Google Places API to add location awareness for more contextual results. Test an API call in your browser and export the code snippet.'),('Kajak','[\"Travel\",\"Transportation\"]','/kajak/1.0.0','[/flights, /hotels, /locations]','API to query realtime Flights prices, Hotels booking and Cars hiring.Create new session for searching flights tickets of all airlines around the world, searching all hotels prices around the world. '),('PayPal','[\"Payments\"]','/paypal/1.0.0','[/createPayment, /executePayment, /sendInvoice, /updatePayment, /getCreditCard]','Accept PayPal and credit card payments online or on mobile. Use the payment resource for direct credit card payments, stored credit card payments, or PayPal account payments.'),('PizzaShackAPI','[\"pizza\",\"check\"]','/pizzashack/1.0.0','[/order, /menu, /order/{orderId}]','This is a RESTFul API for Pizza Shack online pizza delivery store.\r'),('',NULL,NULL,NULL,NULL),('Shopping.com','[\"eCommerce\"]','/shopping.com/1.0.0','[/publisher, /search, /cart]','With the Shopping.com API you can integrate relevant product content with the deepest product catalog available online. Add millions of unique products and merchant offers to your site. Shopping.com, an eBay company, is the world online comparison shoppin'),('Skyscanner Car Hire Live Prices','[\"Cars\",\"Travel\",\"Transportation\"]','/skyscanner-car-hire-live-prices/1.0.0','[/poll-session, /create-session, /information]','Retrieve live prices for car hire providers. Return the details of all possible car hire quotes that satisfy the request query parameters. Prices will be obtained for the car hire quotes during the session. '),('Skyscanner Flight Search','[\"Travel\",\"Transportation\"]','/flightsearch/1.0.0','[/liveflightsearch, /places, /localisation, /browseflightprices]','The Sky Scanner API lets you search for flight & get flight prices from Skyscanners database of prices, as well as get live quotes directly from ticketing agencies.'),('Ticket Master','[\"Events\"]','/ticketmaster/1.0.0','[/getPayments, /searchEvents, /searchVenues]',' Pull events, venues, tickets, deliveries and payments.Find events, venues and filter your search by location, date, availability, and much more. '),('Travel Portal','[\"Travel\",\"Booking\"]','/travel-portal/1.0.0','[/book, /search, /locations]','The Travel Portal API provides programmatic access to functions that allow customers to book hotels, flights, cars, and tours from the developer\'s websites. Travel Portal allows users to make bookings through Expedia, Cartrawler, Dohop, and Viator using i'),('Twitter','[\"Social\",\"Blogging\"]','/twitter/1.0.0','[/search, /message, /ads]','The Twitter micro-blogging service includes two RESTful APIs. The Twitter REST API methods allow developers to access core Twitter data. This includes update timelines, status data, and user information. The Search API methods give developers methods to i'),('Uber Ride','[\"Travel\",\"Transportation\"]','/uber-ride/1.0.0','[/getRide, /payment, /prices]','Request an Uber ride from within your app. Allows retrieving the status of an ongoing or completed trip that was created by your app. '),('Weather','[\"Weather\"]','/weather2020/1.0.0','[/forecast, /timemachine]','This document describe a RESTFul API for Pizza Shack online pizza delivery store.\r'),('',NULL,NULL,NULL,NULL),('Web Search','[\"Data\"]','/web-search/1.0.0','[/autoComplete, /webSearch, /newsSearch]','Web Search API. News API. Image API. Billions of webpages, images and news with a single API call. Build your app for free. Billions of webpages, images and news with a single API call. The API returns a list of relevant results from a search query which '),('WePay','[\"Payment\",\"Finance\"]','/wepay/1.0.0','[/find-account, /account, /create-account]','Integrated payments designed for platforms. Lookup the details of a payment account on WePay.  '),('WordsAPI','[\"Data\"]','/wordsapi/1.0.0','[/search, /synonyms, /antonyms]','Words API lets you retrieve information about English words, including definitions, synonyms, rhymes, pronunciation, syllables, and frequency of usage. you can use Words API to search for words matching parameters you specify.'),('PhoneVerification','[]','/phoneverify/2.0.0','[/CheckPhoneNumber]','');
/*!40000 ALTER TABLE `API_Details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Details`
--

DROP TABLE IF EXISTS `User_Details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User_Details` (
  `User_Name` varchar(255) DEFAULT NULL,
  `APIs` varchar(255) DEFAULT NULL,
  `Tags` varchar(255) DEFAULT NULL,
  `Searches` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Details`
--

LOCK TABLES `User_Details` WRITE;
/*!40000 ALTER TABLE `User_Details` DISABLE KEYS */;
INSERT INTO `User_Details` VALUES ('BettyCooper',NULL,NULL,'Hotels'),('BettyCooper',NULL,'Travel',NULL),('BettyCooper',NULL,NULL,'Booking'),('BettyCooper','Booking',NULL,NULL),('BettyCooper',NULL,NULL,'Hotel Prices'),('BettyCooper',NULL,NULL,'Travel places'),('BettyCooper','Fiz places',NULL,NULL),('BettyCooper','GooglePlaces',NULL,NULL),('BenWalker',NULL,NULL,'Taxi'),('BenWalker',NULL,'Transportation',NULL),('BenWalker',NULL,NULL,'get taxi rides'),('BenWalker',NULL,NULL,'Cars'),('BenWalker',NULL,NULL,'Uber'),('BenWalker','Uber Ride',NULL,NULL),('BenWalker',NULL,NULL,'Pay money'),('BenWalker',NULL,'Payment',NULL),('BenWalker','WePay',NULL,NULL),('BenWalker',NULL,NULL,'Money transactions'),('BenWalker',NULL,NULL,'pay');
/*!40000 ALTER TABLE `User_Details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Subscribed_APIs`
--

DROP TABLE IF EXISTS `User_Subscribed_APIs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User_Subscribed_APIs` (
  `Creator` varchar(255) DEFAULT NULL,
  `App_Name` varchar(255) DEFAULT NULL,
  `API_Name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Subscribed_APIs`
--

LOCK TABLES `User_Subscribed_APIs` WRITE;
/*!40000 ALTER TABLE `User_Subscribed_APIs` DISABLE KEYS */;
INSERT INTO `User_Subscribed_APIs` VALUES ('JaneFox','Test1','PizzaShackAPI'),('ShawnBrown','DefaultApplication','PizzaShackAPI'),('LincolnHolmes','DefaultApplication','PhoneVerification'),('BettyCooper','Grocery Shopping','PayPal'),('BettyCooper','Grocery Shopping','Amazon S3 '),('JessicaLang','Amazon Shopping','Shopping.com');
/*!40000 ALTER TABLE `User_Subscribed_APIs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-06 22:21:31
