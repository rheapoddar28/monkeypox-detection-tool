const dragArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.drag-drop');
let file;
let button = document.querySelector('button');
let input = document.querySelector('input');

button.onclick = () => {
  input.click();
};

//when Browse
input.addEventListener('change', function(){
  file=this.files[0];
  displayFile();
});

//when the file is inside drag area
dragArea.addEventListener('dragover',() => {
  event.preventDefault();
  dragText.textContent='Release to upload';
  dragArea.classList.add('active');
  console.log("File is over drag area");
});

//when the file leaves the drag area
dragArea.addEventListener('dragleave',() => {
  dragText.textContent='Drag & Drop';
  dragArea.classList.remove('active');
  console.log("File is outside drag area");

});

//when the file is dropped in drag area
dragArea.addEventListener('drop',(event)=>{
  event.preventDefault();
  file = event.dataTransfer.files[0];
  dragArea.classlist.add('active');
  displayFile();
});

function displayFile(){
  let fileType = file.type;
  let validExtensions = ['image/jpg','image/jpeg','image/png'];
  if(validExtensions.includes(fileType)){
    let fileReader = new fileReader();

    fileReader.onload = ()=>{
      let fileURL = fileReader.result;
      let imgTag ='<img src="${fileURL}" alt="">';
      dragArea.innerHTML = imgTag;
    }
    fileReader.readAsDataURL(file);
  }else{
    alert('This file is not an image');
    dragArea.classlist.remove('active');
  };
};
