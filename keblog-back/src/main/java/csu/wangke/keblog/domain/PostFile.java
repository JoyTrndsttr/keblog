package csu.wangke.keblog.domain;

import csu.wangke.keblog.utils.FileReadUtil;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class PostFile{
  //status=0代表文章，status=1代表文件夹
  public int status=0;
  public String name;
  public String path;
  public String content;
  public ArrayList<PostFile> postList = new ArrayList<>();
  public FileReadUtil fileReadUtil = new FileReadUtil();

  //constructor
  public PostFile(String path) throws IOException {
    File file = new File(path);
    if(file.listFiles()==null){
      //说明是单个文件(md格式文章)
      this.status = 0;
      this.name = file.getName();
      this.path = file.getPath();
      this.content = fileReadUtil.readFile(path);
    }
    else{
      this.status = 1;
      this.name = file.getName();
      this.path = file.getPath();
      File[] filelist = file.listFiles();
      for(int i=0;i<filelist.length;i++){
//        if(filelist[i].getName().indexOf("DS_Store"))
        this.postList.add(new PostFile((filelist[i].getPath())));//希望内存没事
      }
    }
  }

  public void add(PostFile postFile){
    postList.add(postFile);
  }

  public void delete(int index){

  }

  public PostFile getChild(int index){
    return postList.get(index);
  }

  public ArrayList<PostFile> getAllChild(){
    return postList;
  }

}
