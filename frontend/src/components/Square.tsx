type SquareProps = {
  x: number;
  y: number;
  colour: string;
  id : string
  image?: string;
};

function Square({ x, y, colour, image, id }: SquareProps) {

  function onClick(){
    console.log(`Clicked ${id}`)
  }


  return (
    <div
      className="square"
      id = {id}
      onClick={onClick}
      style={{
        left: `${x}%`,
        top: `${y}%`,
        width: '12.5%',
        height: '12.5%',
        backgroundColor: colour,
      }}
    >
      {image && <img src={image} className="chess-piece" alt="Chess piece" />}
    </div>
  );
}

export default Square;