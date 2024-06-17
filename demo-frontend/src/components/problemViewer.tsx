// problemViewer.js
import { MathpixMarkdown } from "mathpix-markdown-it";
import React, { useMemo } from "react";
import { Col, Row } from "./globalStyled";
const Text = ({ text, align, border, title, disablePink }) => {
  const inSide = useMemo(() => {
    const token = text?.split(" ")?.filter((v) => {
      return v;
    });
    let isBoldOn = false;
    let isItalicOn = false;
    let isUnderlineOn = false;
    return token.map((v, i) => {
      if (v === "<b>") {
        isBoldOn = true;
        return null;
      } else if (v === "</b>") {
        isBoldOn = false;
        return null;
      } else if (v === "<i>") {
        isItalicOn = true;
        return null;
      } else if (v === "</i>") {
        isItalicOn = false;
        return null;
      } else if (v === "<u>") {
        isUnderlineOn = true;
        return null;
      } else if (v === "</u>") {
        isUnderlineOn = false;
        return null;
      } else if (v === "<nl/>") {
        return <div style={{ width: 600, height: 18 }}></div>;
      } else if (v === "<t/>") {
        return (
          <span
            style={{
              fontWeight: isBoldOn ? "bold" : "normal",
              fontStyle: isItalicOn ? "italic" : "normal",
              textDecoration: isUnderlineOn ? "underline" : "none",
              marginLeft: 4,
              marginBottom: 10,
            }}
          >
            ㅤㅤㅤㅤㅤㅤ
          </span>
        );
      } else {
        return (
          <span
            key={i}
            style={{
              fontWeight: isBoldOn ? "bold" : "normal",
              fontStyle: isItalicOn ? "italic" : "normal",
              textDecoration: isUnderlineOn ? "underline" : "none",
              marginLeft: 4,
              backgroundColor:
                v?.length === 1 && !disablePink ? "pink" : "transparent",
              marginBottom: 10,
            }}
          >
            {v}
          </span>
        );
      }
    });
  }, [text]);
  return (
    <div
      style={{
        position: "relative",
        paddingTop: title ? 5 : 0,
        alignItems: "center",
        display: "flex",
      }}
    >
      {title && (
        <div
          style={{
            position: "absolute",
            top: 0,
            width: 600,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <span
            style={{
              backgroundColor: "white",
              display: "flex",
              width: "auto",
              height: 20,
              lineHeight: 1,
              verticalAlign: "sub",
            }}
          >
            {"<"}
            {title}
            {">"}
          </span>
        </div>
      )}
      <Row
        style={{
          height: "auto",
          border: border ? "1px solid black" : "",
          flexWrap: "wrap",
          justifyContent: align,
          width: 600,
          overflow: "visible",
          lineHeight: 1,
          paddingTop: 20,
          paddingBottom: 20,
        }}
      >
        {inSide}
      </Row>
    </div>
  );
};
const Image = ({ url, width }) => {
  return (
    <img
      src={url}
      // https://img-cf.kurly.com/shop/data/goodsview/20201012/gv10000126356_1.jpg
      style={{
        width: width,
        height: "auto",
        objectFit: "contain",
      }}
    />
  );
};
const MathComponent = ({ text, border, title }) => {
  return (
    <div
      style={{
        position: "relative",
        paddingTop: title ? 5 : 0,
        alignItems: "center",
        display: "flex",
        width: 600,
        border: border ? "1px solid black" : "",
      }}
    >
      {title && (
        <div
          style={{
            position: "absolute",
            top: -5,
            width: 600,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <span
            style={{
              backgroundColor: "white",
              display: "flex",
              width: "auto",
              height: 20,
              lineHeight: 1,
              verticalAlign: "sub",
            }}
          >
            {"<"}
            {title}
            {">"}
          </span>
        </div>
      )}
      <MathpixMarkdown text={text} alignMathBlock="start" padding={0} />
    </div>
  );
};
const ProblemViewer = ({ array, width, disablePink }) => {
  return (
    <Col style={{ height: "auto", width: width }}>
      {array.map((v, idx) => {
        const { type, text, align, border, url, math, title } = v;
        if (type === "math") {
          return (
            <MathComponent
              key={idx}
              text={removeNewlinesInMath(math)}
              border={border}
              title={title}
            />
          );
        } else if (type === "image") {
          return <Image key={"image" + idx} width={600} url={url} />;
        } else {
          return (
            <Text
              align={align}
              key={"text" + idx}
              border={border}
              text={text || ""}
              title={title}
              disablePink={disablePink}
            />
          );
        }
      })}
    </Col>
  );
};
export default ProblemViewer;
function removeNewlinesInMath(input) {
  input.split("//g");
  let output = input.replace(/\\[\n\s]*\(/g, "\\(");
  output = output.replace(/\\[\n\s]*\)/g, "\\)");
  return output;
}