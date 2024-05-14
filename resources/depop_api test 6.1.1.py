import os
import json
import csv

# JSON data received from the API
json_data = '''[
{
    "id": 429145373,
    "slug": "goodstuffbyn-womens-nike-dunk-high-retro",
    "url": "https://www.depop.com/products/goodstuffbyn-womens-nike-dunk-high-retro",
    "available": true,
    "dateCreated": "2024-05-13T23:42:48.604698Z",
    "price": {
      "amount": "30.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "goodstuffbyn"
    },
    "images": [
      "https://media-photos.depop.com/b1/16515088/1863183968_2fc80dcc11f34d269064bd9767c60882/P8.jpg",
      "https://media-photos.depop.com/b1/16515088/1863184063_a9e545ab089c4a6b990b3451140cf5f4/P8.jpg",
      "https://media-photos.depop.com/b1/16515088/1863184252_57b535c1b81945a6bc021a36dbae1afd/P8.jpg",
      "https://media-photos.depop.com/b1/16515088/1863184615_2032999bad6c4e70a6135454b36969ca/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 9"
    ]
  },
  {
    "id": 429145113,
    "slug": "krisjji-nike-dunk-low-game-royal",
    "url": "https://www.depop.com/products/krisjji-nike-dunk-low-game-royal",
    "available": true,
    "dateCreated": "2024-05-13T23:41:50.095203Z",
    "price": {
      "amount": "80.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "krisjji"
    },
    "images": [
      "https://media-photos.depop.com/b1/48150850/1863183399_5cda920b2034493ebc5b89c8219883c1/P8.jpg",
      "https://media-photos.depop.com/b1/48150850/1863183431_b1bcb53f8a8547d1ab9257a62f59e13c/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 12"
    ]
  },
  {
    "id": 429144859,
    "slug": "rexi_lynx-nike-dunks-panda-dunks",
    "url": "https://www.depop.com/products/rexi_lynx-nike-dunks-panda-dunks",
    "available": true,
    "dateCreated": "2024-05-13T23:40:52.823891Z",
    "price": {
      "amount": "70.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "rexi_lynx"
    },
    "images": [
      "https://media-photos.depop.com/b1/42081990/1863181721_4be722a7412d487b97aefe29c90d626c/P8.jpg",
      "https://media-photos.depop.com/b1/42081990/1863181768_f59ebb00f3d24647b27d830541dc02a8/P8.jpg",
      "https://media-photos.depop.com/b1/42081990/1863181799_c25867fd58c04774ab299ac431fd5761/P8.jpg",
      "https://media-photos.depop.com/b1/42081990/1863181844_7ff430aedb9a45d9ab2a948b6938b332/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 10.5"
    ]
  },
  {
    "id": 429144619,
    "slug": "ninareese-nike-panda-dunks-size-85",
    "url": "https://www.depop.com/products/ninareese-nike-panda-dunks-size-85",
    "available": true,
    "dateCreated": "2024-05-13T23:39:54.769747Z",
    "price": {
      "amount": "75.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "ninareese"
    },
    "images": [
      "https://media-photos.depop.com/b1/42702938/1863183258_2b4d5429b2154ce286b3a7fd20513e9c/P8.jpg",
      "https://media-photos.depop.com/b1/42702938/1863183282_17fb800b7efa4a4cb98233619889d521/P8.jpg",
      "https://media-photos.depop.com/b1/42702938/1863183299_343a45504c61483c8d59b7bfd9891951/P8.jpg",
      "https://media-photos.depop.com/b1/42702938/1863183308_db14e95603e54ea6aa5574d225c58880/P8.jpg",
      "https://media-photos.depop.com/b1/42702938/1863183326_4c191524b7f64f629b01972a10151ba9/P8.jpg",
      "https://media-photos.depop.com/b1/42702938/1863183345_47b1570d636e439581df88cb032fe7f1/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 8.5"
    ]
  },
  {
    "id": 429144232,
    "slug": "krisjji-nike-low-mystic-red-cargo",
    "url": "https://www.depop.com/products/krisjji-nike-low-mystic-red-cargo",
    "available": true,
    "dateCreated": "2024-05-13T23:38:29.765713Z",
    "price": {
      "amount": "110.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "krisjji"
    },
    "images": [
      "https://media-photos.depop.com/b1/48150850/1863178631_df424658f8f1437a99d7f3488d13304e/P8.jpg",
      "https://media-photos.depop.com/b1/48150850/1863178698_5bcc4aad87354f34993210e7f33bcdc1/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 12"
    ]
  },
  {
    "id": 429144100,
    "slug": "noragrey-michigan-green-dunk-lows-little",
    "url": "https://www.depop.com/products/noragrey-michigan-green-dunk-lows-little",
    "available": true,
    "dateCreated": "2024-05-13T23:38:01.617508Z",
    "price": {
      "amount": "400.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "noragrey"
    },
    "images": [
      "https://media-photos.depop.com/b1/48777768/1863177002_d59ab9b082304cc2b20f5e0adf988902/P8.jpg",
      "https://media-photos.depop.com/b1/48777768/1863177278_7ab7ae7a8a0048978442b06cf66d2f96/P8.jpg",
      "https://media-photos.depop.com/b1/48777768/1863177606_12a99e64422f46f984da2579c6a74bb2/P8.jpg",
      "https://media-photos.depop.com/b1/48777768/1863177854_3b6371261c0d49ed835a6d937340b36b/P8.jpg",
      "https://media-photos.depop.com/b1/48777768/1863178035_667e53c18c184eb59df9a9c99dac1783/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 8"
    ]
  },
  {
    "id": 429142637,
    "slug": "audieringo-air-jordan-one-take-3-7740",
    "url": "https://www.depop.com/products/audieringo-air-jordan-one-take-3-7740",
    "available": true,
    "dateCreated": "2024-05-13T23:32:46.669697Z",
    "price": {
      "amount": "145.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "13.49",
      "internationalShipping": "30.00"
    },
    "seller": {
      "username": "audieringo"
    },
    "images": [
      "https://media-photos.depop.com/b1/40231962/1863173296_922b894e13234cae9fc9b6f5b422a133/P8.jpg",
      "https://media-photos.depop.com/b1/40231962/1863173330_7193391c200b44be9af55c97eaefa363/P8.jpg",
      "https://media-photos.depop.com/b1/40231962/1863173364_1f229b516ef448bda10e9c6e6e72594e/P8.jpg",
      "https://media-photos.depop.com/b1/40231962/1863173394_472baaa09bb9404eae2452e6493f21ca/P8.jpg",
      "https://media-photos.depop.com/b1/40231962/1863173429_234c864bf5ad42a0b3f8e4b0a157c7cf/P8.jpg",
      "https://media-photos.depop.com/b1/40231962/1863173460_5bfc3ac0577a490b8ece4be9c4175506/P8.jpg",
      "https://media-photos.depop.com/b1/40231962/1863173549_28ab85d2d8d84f1dbccbfe2f59a12624/P8.jpg",
      "https://media-photos.depop.com/b1/40231962/1863173618_e9c12e5746974c6f8e633ee6a7921780/P8.jpg"
    ],
    "brand": "Jordan",
    "sizes": [
      "US 10"
    ]
  },
  {
    "id": 429142498,
    "slug": "illusionsupply-nike-sb-dunk-low-concepts",
    "url": "https://www.depop.com/products/illusionsupply-nike-sb-dunk-low-concepts",
    "available": true,
    "dateCreated": "2024-05-13T23:32:11.943545Z",
    "price": {
      "amount": "345.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "7.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "illusionsupply"
    },
    "images": [
      "https://media-photos.depop.com/b1/46863340/1863169894_926bb1c00a0b4a6cb4945efb92890b67/P8.jpg",
      "https://media-photos.depop.com/b1/46863340/1863169889_a9131fb53f434c1083e18ea42093c0d5/P8.jpg",
      "https://media-photos.depop.com/b1/46863340/1863169887_75a47bd4795345d883bdfea743c3c358/P8.jpg",
      "https://media-photos.depop.com/b1/46863340/1863169888_af6a0ccba9644c5ab3638ac74cc9bace/P8.jpg",
      "https://media-photos.depop.com/b1/46863340/1863169896_c6e9364215b84836bd05b2eaded2afd1/P8.jpg",
      "https://media-photos.depop.com/b1/46863340/1863169886_195affe3a5bf4e4a95b71ae813d3b7e4/P8.jpg",
      "https://media-photos.depop.com/b1/46863340/1863169892_40f9d8854d11414cbadea322d8489c9d/P8.jpg",
      "https://media-photos.depop.com/b1/46863340/1863169893_3e7002605cab41fc8a0c9c6fc4279f06/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 8.5"
    ]
  },
  {
    "id": 429142479,
    "slug": "765_johnny-court-purple-nike-dunks-size",
    "url": "https://www.depop.com/products/765_johnny-court-purple-nike-dunks-size",
    "available": true,
    "dateCreated": "2024-05-13T23:32:07.847555Z",
    "price": {
      "amount": "80.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "765_johnny"
    },
    "images": [
      "https://media-photos.depop.com/b1/46376107/1863166101_3f8c60825e784cd08317918f5a918b88/P8.jpg",
      "https://media-photos.depop.com/b1/46376107/1863166806_77e8cb3c39d442e098ed42957f9b7bf0/P8.jpg",
      "https://media-photos.depop.com/b1/46376107/1863167321_63295e68abca4eb4b5ea0f75bdbc7bd9/P8.jpg",
      "https://media-photos.depop.com/b1/46376107/1863168757_c9729f7b0beb4cbb8051babf5c98a708/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 11"
    ]
  },
  {
    "id": 429142000,
    "slug": "mackenziewilliams104-nike-high-top-dunks",
    "url": "https://www.depop.com/products/mackenziewilliams104-nike-high-top-dunks",
    "available": true,
    "dateCreated": "2024-05-13T23:30:16.431639Z",
    "price": {
      "amount": "90.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "mackenziewilliams104"
    },
    "images": [
      "https://media-photos.depop.com/b1/35566269/1863169982_831e3f707504421e90b687019e008d84/P8.jpg",
      "https://media-photos.depop.com/b1/35566269/1863170044_a2b4f3afaff04347b84b449074b27d7b/P8.jpg",
      "https://media-photos.depop.com/b1/35566269/1863170092_0245856c004b4a07b1ba78a7025fe8ba/P8.jpg",
      "https://media-photos.depop.com/b1/35566269/1863170122_cff70fc8f0624a67831b4d498b0985a2/P8.jpg",
      "https://media-photos.depop.com/b1/35566269/1863170148_4dbedc080cc34fff8387ce935a5b6b4d/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 8"
    ]
  },
  {
    "id": 429141690,
    "slug": "ketuttle-size-9-nike-dunk-premium",
    "url": "https://www.depop.com/products/ketuttle-size-9-nike-dunk-premium",
    "available": true,
    "dateCreated": "2024-05-13T23:29:07.04227Z",
    "price": {
      "amount": "350.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "13.49",
      "internationalShipping": null
    },
    "seller": {
      "username": "ketuttle"
    },
    "images": [
      "https://media-photos.depop.com/b1/46344530/1863169599_5586fd568b48488c81f5fb2ba67329cd/P8.jpg",
      "https://media-photos.depop.com/b1/46344530/1863169618_04d38491c855492a8b5fc154f3def73b/P8.jpg",
      "https://media-photos.depop.com/b1/46344530/1863169626_55220f0aeb9749699aaeb0139a5401c4/P8.jpg",
      "https://media-photos.depop.com/b1/46344530/1863169636_da49f76c4e87431db7681b365153f40c/P8.jpg",
      "https://media-photos.depop.com/b1/46344530/1863169650_a1c1987afe7a4c0cb7163c2f865192b3/P8.jpg",
      "https://media-photos.depop.com/b1/46344530/1863169666_60ed60d624544132bc2e32465a6a8f3e/P8.jpg",
      "https://media-photos.depop.com/b1/46344530/1863169674_7f37d51c513a400d85446976d54375b5/P8.jpg",
      "https://media-photos.depop.com/b1/46344530/1863169690_e1f9d4b50e224b498661a7213abcb636/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 9"
    ]
  },
  {
    "id": 429140759,
    "slug": "ajlakk-panda-dunks",
    "url": "https://www.depop.com/products/ajlakk-panda-dunks",
    "available": true,
    "dateCreated": "2024-05-13T23:25:24.906839Z",
    "price": {
      "amount": "30.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "ajlakk"
    },
    "images": [
      "https://media-photos.depop.com/b1/47008035/1863164485_b44826e913dc4b0cb06720ae5955aa55/P8.jpg",
      "https://media-photos.depop.com/b1/47008035/1863164513_7ee4316c80ec45b39f6ad5d7a426811e/P8.jpg",
      "https://media-photos.depop.com/b1/47008035/1863164527_9b742291b9eb40a7a081252b29221693/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 9.5"
    ]
  },
  {
    "id": 429139684,
    "slug": "cgrey411-nike-dunk-low-premium-wolf",
    "url": "https://www.depop.com/products/cgrey411-nike-dunk-low-premium-wolf",
    "available": true,
    "dateCreated": "2024-05-13T23:21:13.056858Z",
    "price": {
      "amount": "75.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "cgrey411"
    },
    "images": [
      "https://media-photos.depop.com/b1/44891222/1863157203_7135685e6412400f97eb13a45fbb49e6/P8.jpg",
      "https://media-photos.depop.com/b1/44891222/1863157294_5160de1a8541486e90c862f77c3cfc6e/P8.jpg",
      "https://media-photos.depop.com/b1/44891222/1863157332_4e142cf5be8e4114bb7ea373fea23973/P8.jpg",
      "https://media-photos.depop.com/b1/44891222/1863157406_834c3f8f8fdc41698191fb24acee5720/P8.jpg",
      "https://media-photos.depop.com/b1/44891222/1863157455_5b26794c1d7d4b80bb0e1f6a95184851/P8.jpg",
      "https://media-photos.depop.com/b1/44891222/1863157868_a8957eb345764041a3844a42d00b7a54/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 11.5"
    ]
  },
  {
    "id": 429138580,
    "slug": "annyshop-name-nike-renew-arena-plum-1050",
    "url": "https://www.depop.com/products/annyshop-name-nike-renew-arena-plum-1050",
    "available": true,
    "dateCreated": "2024-05-13T23:17:10.839569Z",
    "price": {
      "amount": "47.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "7.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "annyshop"
    },
    "images": [
      "https://media-photos.depop.com/b1/29487631/1863154945_85dfb316382c455692174d8979585630/P8.jpg",
      "https://media-photos.depop.com/b1/29487631/1863154983_16dfb1e9e7f64b36829902daf1a648d1/P8.jpg",
      "https://media-photos.depop.com/b1/29487631/1863155018_f7c0a5b2b26d4a56a996571ae0015a9f/P8.jpg",
      "https://media-photos.depop.com/b1/29487631/1863155050_c4420bf214964b64ad9b35289425b329/P8.jpg",
      "https://media-photos.depop.com/b1/29487631/1863155086_feefecc15f234b1dad5e876b7c318170/P8.jpg",
      "https://media-photos.depop.com/b1/29487631/1863155117_2508a5f358b847e79ac3914afa2d0a7c/P8.jpg",
      "https://media-photos.depop.com/b1/29487631/1863155159_1ad0e38a64c1467aa1cf353000e85a08/P8.jpg",
      "https://media-photos.depop.com/b1/29487631/1863155207_f28a2ae3cf32438f94c6992bac1c9103/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 10"
    ]
  },
  {
    "id": 429136204,
    "slug": "chriscloset123-dunk-high-australia-mens-size",
    "url": "https://www.depop.com/products/chriscloset123-dunk-high-australia-mens-size",
    "available": true,
    "dateCreated": "2024-05-13T23:07:29.638176Z",
    "price": {
      "amount": "60.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "4.49",
      "internationalShipping": null
    },
    "seller": {
      "username": "chriscloset123"
    },
    "images": [
      "https://media-photos.depop.com/b1/46355956/1863141958_7eab0ea21749491bae181732cf609fc1/P8.jpg",
      "https://media-photos.depop.com/b1/46355956/1863142053_6d36ae94401a449eb59f52245c0f06b1/P8.jpg",
      "https://media-photos.depop.com/b1/46355956/1863142140_3af74a1610524eb6b9b57e3d592967fc/P8.jpg",
      "https://media-photos.depop.com/b1/46355956/1863142240_e21c6d77a5524b70b63e068dfdba1345/P8.jpg",
      "https://media-photos.depop.com/b1/46355956/1863142333_3123ca448e334dc987f172d1f5ff10a1/P8.jpg",
      "https://media-photos.depop.com/b1/46355956/1863142401_a5461131e35143d09029096ed45ef163/P8.jpg",
      "https://media-photos.depop.com/b1/46355956/1863142427_cc6d3d27ddae414da528669b0ac7ac96/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 10"
    ]
  },
  {
    "id": 429136059,
    "slug": "blakeroberson-nike-panda-dunks-size-115",
    "url": "https://www.depop.com/products/blakeroberson-nike-panda-dunks-size-115",
    "available": true,
    "dateCreated": "2024-05-13T23:07:03.092365Z",
    "price": {
      "amount": "55.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "blakeroberson"
    },
    "images": [
      "https://media-photos.depop.com/b1/29347458/1863140210_1dcff064e0344ff4bfeb722b2e1a28e9/P8.jpg",
      "https://media-photos.depop.com/b1/29347458/1863140473_fd7bd898fb3d4dba8288cc98d69dce9b/P8.jpg",
      "https://media-photos.depop.com/b1/29347458/1863140636_1069ccfe0b9849209f70abbf0b80caf7/P8.jpg",
      "https://media-photos.depop.com/b1/29347458/1863140847_886778d7bc5c41e88b29d11360274b63/P8.jpg",
      "https://media-photos.depop.com/b1/29347458/1863141369_8faa15701c3c4def93a45c9d23a174cc/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 11.5"
    ]
  },
  {
    "id": 429135988,
    "slug": "xozariya16-green-dunks-with-new",
    "url": "https://www.depop.com/products/xozariya16-green-dunks-with-new",
    "available": true,
    "dateCreated": "2024-05-13T23:06:44.640738Z",
    "price": {
      "amount": "85.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "xozariya16"
    },
    "images": [
      "https://media-photos.depop.com/b1/35154241/1863141907_c695a5eac2ba4f058d81f5e1d89c92cf/P8.jpg",
      "https://media-photos.depop.com/b1/35154241/1863141929_0dbfd559809644f6a39f7fe613b8db30/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 6"
    ]
  },
  {
    "id": 429135729,
    "slug": "ric_flair-nike-dunk-lows-cream-white",
    "url": "https://www.depop.com/products/ric_flair-nike-dunk-lows-cream-white",
    "available": true,
    "dateCreated": "2024-05-13T23:05:45.297522Z",
    "price": {
      "amount": "25.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "6.29",
      "internationalShipping": null
    },
    "seller": {
      "username": "ric_flair"
    },
    "images": [
      "https://media-photos.depop.com/b1/44578245/1863137144_b1c51f12766e46209fd43fc5692082a1/P8.jpg",
      "https://media-photos.depop.com/b1/44578245/1863137213_a69315b217114c2dafa70a217eeebaac/P8.jpg",
      "https://media-photos.depop.com/b1/44578245/1863137246_f27290a8043447b1b7659b26a20dafe6/P8.jpg",
      "https://media-photos.depop.com/b1/44578245/1863137319_e1795c886e4d4e71a043c6fca6cebc22/P8.jpg",
      "https://media-photos.depop.com/b1/44578245/1863137379_4e121175b9e04341a3d7d04148485c73/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 10"
    ]
  },
  {
    "id": 429133345,
    "slug": "darionnandlal-nike-dunks-green-and-yellow",
    "url": "https://www.depop.com/products/darionnandlal-nike-dunks-green-and-yellow",
    "available": true,
    "dateCreated": "2024-05-13T22:56:56.861539Z",
    "price": {
      "amount": "45.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "darionnandlal"
    },
    "images": [
      "https://media-photos.depop.com/b1/42604798/1863129550_58cb6485f78741968a9b9af89118fb6a/P8.jpg",
      "https://media-photos.depop.com/b1/42604798/1863129602_aa8f27bc8aed4a9390a397d32019806e/P8.jpg",
      "https://media-photos.depop.com/b1/42604798/1863129675_3cec0e6b047a4915bae3ec8d74332135/P8.jpg",
      "https://media-photos.depop.com/b1/42604798/1863129724_b911d41c7ca340f29d31d0a5f4f4733b/P8.jpg",
      "https://media-photos.depop.com/b1/42604798/1863129785_bf2f5af4b0564583ad1c167cd5b11f84/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 9"
    ]
  },
  {
    "id": 429132982,
    "slug": "xozariya16-pink-prism-dunks-worn-for",
    "url": "https://www.depop.com/products/xozariya16-pink-prism-dunks-worn-for",
    "available": true,
    "dateCreated": "2024-05-13T22:55:33.699307Z",
    "price": {
      "amount": "55.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "xozariya16"
    },
    "images": [
      "https://media-photos.depop.com/b1/35154241/1863121693_988744509040447f93993b7e09cd4f3a/P8.jpg",
      "https://media-photos.depop.com/b1/35154241/1863121738_097d643e521146ca913f51ed26eebc9c/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 6"
    ]
  },
  {
    "id": 429132951,
    "slug": "noahajacobson22-nike-dunk-high-never-worn",
    "url": "https://www.depop.com/products/noahajacobson22-nike-dunk-high-never-worn",
    "available": true,
    "dateCreated": "2024-05-13T22:55:28.580106Z",
    "price": {
      "amount": "110.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "noahajacobson22"
    },
    "images": [
      "https://media-photos.depop.com/b1/20145560/1863128181_22d68b81738d48dab2141416ee704252/P8.jpg",
      "https://media-photos.depop.com/b1/20145560/1863128241_8a7c1503e37142f6a295c4e62d326da4/P8.jpg",
      "https://media-photos.depop.com/b1/20145560/1863128304_5923851ecde14d689b7c60abe16b996f/P8.jpg",
      "https://media-photos.depop.com/b1/20145560/1863128333_5152b44ad3054dfda3ea92dc993bcd36/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 12"
    ]
  },
  {
    "id": 429132919,
    "slug": "bloodyej24-nike-dunks-light-carbon",
    "url": "https://www.depop.com/products/bloodyej24-nike-dunks-light-carbon",
    "available": true,
    "dateCreated": "2024-05-13T22:55:19.366344Z",
    "price": {
      "amount": "67.54",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": "10.99"
    },
    "seller": {
      "username": "bloodyej24"
    },
    "images": [
      "https://media-photos.depop.com/b1/48825848/1863059146_6a2fe14607854f23bb180b5d30c505a3/P8.jpg",
      "https://media-photos.depop.com/b1/48825848/1863059199_3822ec14cbe649fc89297dd288d95461/P8.jpg",
      "https://media-photos.depop.com/b1/48825848/1863059242_ea3e7dbbe5cd41e1bf4aece859e4a8ce/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 9"
    ]
  },
  {
    "id": 429132520,
    "slug": "naynay0116-orange-dunks-womens-85-worn",
    "url": "https://www.depop.com/products/naynay0116-orange-dunks-womens-85-worn",
    "available": true,
    "dateCreated": "2024-05-13T22:53:44.693386Z",
    "price": {
      "amount": "95.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "10.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "naynay0116"
    },
    "images": [
      "https://media-photos.depop.com/b1/38779685/1863126405_15f4270d3ba045b49a15b64300213c3e/P8.jpg",
      "https://media-photos.depop.com/b1/38779685/1863126428_2104181c55fe4135b8f6b882b77f9533/P8.jpg",
      "https://media-photos.depop.com/b1/38779685/1863126459_612cca922c4741e7b5d8e5a5e387c3e7/P8.jpg",
      "https://media-photos.depop.com/b1/38779685/1863126479_514b5121efb247b4b615b606e947417b/P8.jpg",
      "https://media-photos.depop.com/b1/38779685/1863126614_0c6a1557e5ff406c9e59d5d6b8c4c2ff/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 8.5"
    ]
  },
  {
    "id": 429131802,
    "slug": "palmtreegod-nike-dunk-high-off-white",
    "url": "https://www.depop.com/products/palmtreegod-nike-dunk-high-off-white",
    "available": true,
    "dateCreated": "2024-05-13T22:50:49.433462Z",
    "price": {
      "amount": "50.00",
      "amountWithTax": null,
      "discount": null,
      "currency": "USD",
      "nationalShipping": "7.99",
      "internationalShipping": null
    },
    "seller": {
      "username": "palmtreegod"
    },
    "images": [
      "https://media-photos.depop.com/b1/6295381/1863054177_0eb9a4a5e4db45f5bc392d2896fd00ba/P8.jpg",
      "https://media-photos.depop.com/b1/6295381/1863054446_f9ff1258c755487f876e4cc6a5b4b389/P8.jpg",
      "https://media-photos.depop.com/b1/6295381/1863054970_e7f15da324284726ab37f98d62ea3262/P8.jpg",
      "https://media-photos.depop.com/b1/6295381/1863055245_a0f02047a65e4d8d9d4961c1a2902cc6/P8.jpg",
      "https://media-photos.depop.com/b1/6295381/1863055624_7d2d64546dde4d7b90d8803d452e9d22/P8.jpg"
    ],
    "brand": "Nike",
    "sizes": [
      "US 4.5"
    ]
  }
]'''

# Parse JSON data into a Python object
data = json.loads(json_data)

# Specify CSV file path
csv_file_path = "/Users/rymac/PycharmProjects/pythonProject/depop_api_test_6/depop_data.csv"

# Create directory if it doesn't exist
directory = os.path.dirname(csv_file_path)
if not os.path.exists(directory):
    os.makedirs(directory)

# Define column names for the CSV file (excluding 'images')
column_names = ['id', 'slug', 'url', 'available', 'dateCreated', 'price', 'seller', 'brand', 'sizes']

# Write data to CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=column_names)
    writer.writeheader()
    for item in data:
        # Remove 'images' key from the item dictionary
        item.pop('images', None)
        writer.writerow(item)
