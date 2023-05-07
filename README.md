<a name="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/HyScript7/ProCM">
    <img src="app/static/img/logo.svg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">ProCM</h3>

  <p align="center">
    G+SOŠ Seminar Work 2023
    <br />
    <a href="https://docs.google.com/document/d/1NuqVESW1STSTG-GhvvjajzcHyAzxAaAm92JQLKchdXs/edit?usp=sharing"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/HyScript7/ProCM">View Demo</a>
    ·
    <a href="https://github.com/HyScript7/ProCM/issues">Report Bug</a>
    ·
    <a href="https://github.com/HyScript7/ProCM/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Seminar work for the year 2023. It's a blog & project galery application written in the flask framework for python using MongoDB as it's back-end database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][python-shield]][python-url]
* [![Flask][flask-shield]][flask-url]
* [![MongoDB][mongo-shield]][mongo-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy of ProCM up and running follow these simple steps.

### Prerequisites

To run the server, you need a MongoDB database and python installed on your host device.

* [mongodb database](https://www.mongodb.com/)
* [python >= 3.10](https://www.python.org/)
* pip
  ```sh
  pip install --upgrade pip
  ```

### Installation

1. Get credentials to your MongoDB database (or setup one before hand if you don't have one)
2. Clone the repo
   ```sh
   git clone https://github.com/HyScript7/ProCM.git
   ```
3. Install  pip requirements
   ```sh
   pip install -r ./app/requirements.txt
   ```
4. Configure credentials and application in `.env`

| Property                | Used for                                                 |
| ----------------------- | -------------------------------------------------------- |
| PASSWORD_SECRET         | Salting password hashes                                  |
| FLASK_SECRET            | Encrypting session cookie                                |
| FLASK_SESSION_LIFETIME  | How long until the session cookie expires                |
| MONGO_HOST              | Mongo Database Host                                      |
| MONGO_PORT              | Mongo Database Port                                      |
| MONGO_USER              | Mongo Database Username                                  |
| MONGO_PASS              | Mongo Database Password                                  |
| MONGO_SRV               | Whether MongoDB address is using the srv protocol or not |
| PCM_DATABASE            | Name of the database to use                              |
| PCM_COLLECTION_USERS    | Which collection (table) to store users in               |
| PCM_COLLECTION_GROUPS   | Which collection to store permission groups in           |
| PCM_COLLECTION_PROJECTS | This is not used                                         |
| PCM_COLLECTION_POSTS    | Which collection to store blog posts in                  |
| PCM_COLLECTION_COMMENTS | Which collection to store blog comments in               |
| REGISTRATION            | Whether to enable registration or not (true/false)       |
| BRAND                   | The name of the site                                     |
| GIT_TOKEN               | The github token to fetch projects with                  |
| GIT_USERNAME            | The github username of the account that owns the token   |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

For instructions on how to use ProCM, please reffer to the [Documentation](https://docs.google.com/document/d/1NuqVESW1STSTG-GhvvjajzcHyAzxAaAm92JQLKchdXs/edit?usp=sharing)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Authentication
- [x] Blog
- [x] User profile "About me"
    - [x] Bio Editor
- [ ] Project galery
	- [ ] Image galery
- [ ] Admin Panel
	- [ ] User Management
	- [ ] Blog Management
	- [ ] Project Management (Might be removed in the future)
- [ ] TOS/Privacy Docs
- [ ] Documentation
- [ ] v3 API

See the [open issues](https://github.com/HyScript7/ProCM/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. While contributions are welcome, they are not neccesary, as this project is a mess and will most likely get a complete rewrite if it is to be used sometime in the future.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Štefan Prokop - [@hyscript7](https://twitter.com/hyscript7) - hyscript7@gmail.com

Project Link: [https://github.com/HyScript7/ProCM](https://github.com/HyScript7/ProCM)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Trello](https://trello.com)
* [Bootstrap Docs](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
* [Shields.io](https://shields.io/)
* [ReadMe Template](https://github.com/othneildrew/Best-README-Template/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/HyScript7/ProCM.svg?style=for-the-badge
[contributors-url]: https://github.com/HyScript7/ProCM/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/HyScript7/ProCM.svg?style=for-the-badge
[forks-url]: https://github.com/HyScript7/ProCM/network/members
[stars-shield]: https://img.shields.io/github/stars/HyScript7/ProCM.svg?style=for-the-badge
[stars-url]: https://github.com/HyScript7/ProCM/stargazers
[issues-shield]: https://img.shields.io/github/issues/HyScript7/ProCM.svg?style=for-the-badge
[issues-url]: https://github.com/HyScript7/ProCM/issues
[license-shield]: https://img.shields.io/github/license/HyScript7/ProCM.svg?style=for-the-badge
[license-url]: https://github.com/HyScript7/ProCM/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[flask-shield]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/2.3.x/
[mongo-shield]: https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white
[mongo-url]: https://www.mongodb.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
