scalaVersion := "2.12.4"

// These settings will be used by each of the subprojects
lazy val commonSettings = Seq(
  organization := "nzaman",
  version := "1.0",
  scalaVersion := "2.12.4"
)

lazy val root = (project in file("."))
    .aggregate(common, trie, linkedlist)
  .settings(
    commonSettings,
    name := "scala-data-structures"
  )

lazy val common = (project in file("common"))
    .settings(
      commonSettings,
      name := "common"
    )

lazy val trie = (project in file("trie"))
  .settings(
    commonSettings,
    name := "trie"
  ).dependsOn(common)

lazy val linkedlist = (project in file("linked-list"))
  .settings(
    commonSettings,
    name := "linked-list"
  ).dependsOn(common)

// Places for sbt to look for library dependencies.
// See http://www.scala-sbt.org/1.x/docs/Resolvers.html for some more basic resolvers
resolvers ++= Seq(
  DefaultMavenRepository,
  Resolver.defaultLocal,
  Resolver.mavenLocal
)

// You can use Scaladex, an index of all known published Scala libraries. There,
// after you find the library you want, you can just copy/paste the dependency
// information that you need into your build file. For example, on the
// typelevel/cats Scaladex page,
// https://index.scala-lang.org, you can copy/paste the sbt
// dependency from the sbt box on the right-hand side of the screen.

// To learn more about sbt, head over to the official sbt
// documentation at http://www.scala-sbt.org/documentation.html

